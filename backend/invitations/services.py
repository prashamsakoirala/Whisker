from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import Optional
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from .schemas import InvitationCreate, InvitationResponse, InvitationTokenPayload, InvitationTokenDecoded, InvitationDisplay
from .invitations import create_invitation_token, decode_invitation_token
from .types import InvitationStatus
from .config import INVITATION_TOKEN_EXPIRE_MINUTES, EMAIL, APP_PASSWORD
from .crud import update_invitation_status, get_invitation_by_code, get_most_recent_invitation_by_emails, create_invitation
from users.crud import get_user, get_user_by_email
import smtplib
from email.mime.text import MIMEText


def generate_and_send_invitation(db: Session, invitation_data: InvitationCreate) -> InvitationResponse:
    inviter = get_user_by_email(db, invitation_data.inviter_email)
    if not inviter:
        raise ValueError("Inviter not found")
    
    inviter_email = inviter.email
    inviter_photo_url = inviter.profile_picture
    inviter_name = inviter.name
    inviter_id = inviter.user_id

    invitee_email = invitation_data.invitee_email

    if inviter_email == invitee_email:
        raise ValueError("Cannot send invitation to yourself")

    existing_invitation = get_most_recent_invitation_by_emails(db, invitee_email, inviter_email)

    if existing_invitation:
        if existing_invitation.status == InvitationStatus.PENDING:
            raise ValueError("Invitation already sent and pending")
        
        if existing_invitation.status == InvitationStatus.ACCEPTED:
            raise ValueError("Invitation already accepted")
    
    invitation_token = create_invitation_token(InvitationTokenPayload(invitee_email=invitee_email, inviter_email=inviter_email))
    
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=INVITATION_TOKEN_EXPIRE_MINUTES)
    # adds to database
    create_invitation(db, inviter_id, invitee_email, invitation_token, INVITATION_TOKEN_EXPIRE_MINUTES)
    
    invitation_link = generate_invitation_link(invitation=invitation_token)
    send_invitation_email(invitation_link=invitation_link, invitee_email=invitee_email, inviter_name=inviter_name, inviter_photo_url=inviter_photo_url)

    return InvitationResponse(invitee_email=invitee_email, inviter_email=inviter_email, status=InvitationStatus.PENDING, expires_at=expires_at)


def get_invitation_information(db: Session, invitation_code: str, verifier_email: EmailStr) -> InvitationDisplay:
    verify_invitee(db=db, token=invitation_code, verifier_email=verifier_email)
    invitation = get_invitation_by_code(db, invitation_code)
    
    inviter = get_user(db, invitation.inviter_id)
    if not inviter:
        raise ValueError("Inviter not found")

    invitee = get_user_by_email(db, verifier_email)
    if not invitee:
        raise ValueError("Invitee not found")

    return InvitationDisplay(invitee_email=invitation.invitee_email, inviter_email=inviter.email,status=invitation.status,expires_at=invitation.expires_at,inviter_name=inviter.name, invitee_name=invitee.name, inviter_picture=inviter.profile_picture or "", invitee_picture=invitee.profile_picture or "")

def verify_invitee(db: Session, token: str, verifier_email: EmailStr) -> InvitationResponse:
    invitation = verify_invitation_token(db, token)
    if invitation.invitee_email != verifier_email:
        raise ValueError("Invalid user")
    invitee_user = get_user_by_email(db, verifier_email)
    if not invitee_user:
        raise ValueError("User not found")
    return InvitationResponse(invitee_email=invitation.invitee_email, inviter_email=invitation.inviter_email, status=InvitationStatus.PENDING, expires_at=invitation.expires_at)

def verify_inviter(db: Session, token: str, verifier_email: EmailStr) -> InvitationResponse:
    invitation = verify_invitation_token(db, token)
    if invitation.inviter_email != verifier_email:
        raise ValueError("Invalid user")
    inviter_user = get_user_by_email(db, verifier_email)
    if not inviter_user:
        raise ValueError("User not found")
    return InvitationResponse(invitee_email=invitation.invitee_email, inviter_email=invitation.inviter_email, status=InvitationStatus.PENDING, expires_at=invitation.expires_at)


def verify_invitation_token(db: Session, token: str) -> InvitationTokenDecoded:
    decoded_token = decode_invitation_token(token=token) # returns InvitationTokenDecoded with expires_at
    invitation = get_invitation_by_code(db, token)
    if not invitation:
        raise ValueError("Invalid invitation")
    if invitation.status != InvitationStatus.PENDING:
        raise ValueError("Invitation is not pending")
    return decoded_token

# check if pending before accepting in routes layer
def accept_invitation(db: Session, token: str, invitee_email: str) -> InvitationResponse:
    verification = verify_invitation_token(db, token)
    if not verification:
        raise ValueError("Invalid invitation")

    if not verify_invitee(db=db, token=token, verifier_email=invitee_email):
        raise ValueError("Invalid user")
        
    updated_invitation = update_invitation_status(db, token, InvitationStatus.ACCEPTED)
    return InvitationResponse(invitee_email=updated_invitation.invitee_email, inviter_email=get_user(db, updated_invitation.inviter_id).email, status=updated_invitation.status, expires_at=updated_invitation.expires_at)


def decline_invitation(db: Session, invitation_code: str, invitee_email: str) -> InvitationResponse:
    verification = verify_invitation_token(db, invitation_code)
    if not verification:
        raise ValueError("Invalid invitation")

    if not verify_invitee(db=db, token=invitation_code, verifier_email=invitee_email):
        raise ValueError("Invalid user")

    updated_invitation = update_invitation_status(db, invitation_code, InvitationStatus.DECLINED)
    return InvitationResponse(invitee_email=updated_invitation.invitee_email, inviter_email=get_user(db, updated_invitation.inviter_id).email, status=updated_invitation.status, expires_at=updated_invitation.expires_at)

# only can be used by inviter to revoke
def revoke_invitation(db: Session, invitation_code: str, inviter_email: str) -> InvitationResponse:
    verification = verify_invitation_token(db, invitation_code)
    if not verification:
        raise ValueError("Invalid invitation")

    if not verify_inviter(db=db, token=invitation_code, verifier_email=inviter_email):
        raise ValueError("Invalid user")

    updated_invitation = update_invitation_status(db, invitation_code, InvitationStatus.REVOKED)
    return InvitationResponse(invitee_email=updated_invitation.invitee_email, inviter_email=get_user(db, updated_invitation.inviter_id).email, status=updated_invitation.status, expires_at=updated_invitation.expires_at)

# Validate in routes?
def validate_google_email(email: str) -> bool:
    allowed_domains = ['@gmail.com', '@googlemail.com']
    return any(email.lower().endswith(domain) for domain in allowed_domains)

def hash_invitation_code(code: str) -> str:
    pass

# def if the user is not authorized then redirect url to login?
# i think there needs to be an endpoint and then redirect it back to the invitation
# how would this work?

def generate_invitation_link(invitation: str):
    return f"http://localhost:8000/invitations?code={invitation}"

# mailchimp inviation flow? or can i not just send it
def send_invitation_email(invitee_email: str, invitation_link: str, inviter_name: str, inviter_photo_url: Optional[str] = None) -> None:
    if not EMAIL or not APP_PASSWORD:
        raise ValueError("EMAIL and APP_PASSWORD environment variables must be set")

    msg = MIMEText(f"Hi! {inviter_name} has invited you to raise a pet with them! Click here to join: {invitation_link}")
    msg["Subject"] = "Someone invited you to Whisker!"
    msg["From"] = f"Whisker <{EMAIL}>"
    msg["To"] = invitee_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)
    

# def verify invitation gmail?


# #### TEST TEST TEST TEST ####
# # Can make it better with no-reply but its fine

# @router.post("/api/send-invitation")
# async def send_invitation(email: str):
#     try:
#         send_invite_email(email)
#         return {"message": "Invitation sent successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send invitation: {str(e)}")


# def send_invite_email(recipient_email):
#     """
#     Send an invitation email to the specified recipient.
#     Raises ValueError if EMAIL or APP_PASSWORD are not configured.
#     """
#     if not EMAIL or not APP_PASSWORD:
#         raise ValueError("EMAIL and APP_PASSWORD environment variables must be set")
    
#     msg = MIMEText(f"Hi! Click here to join:")
#     msg["Subject"] = "You're invited to Whisker!"
#     msg["From"] = f"Whisker <{EMAIL}>"
#     msg["To"] = recipient_email

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(EMAIL, APP_PASSWORD)
#         server.send_message(msg)

# #### TEST TEST TEST TEST ####