from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import Optional
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from .schemas import InvitationCreate, InvitationResponse, InvitationTokenPayload
from .invitations import create_invitation_token, decode_invitation_token
from .types import InvitationStatus
from .config import SALT, INVITATION_TOKEN_EXPIRE_MINUTES
from .crud import update_invitation_status, get_invitation_by_code, get_most_recent_invitation_by_emails, create_invitation
from users.crud import get_user, get_user_by_email


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
    create_invitation(db, inviter_id, invitee_email, invitation_token, INVITATION_TOKEN_EXPIRE_MINUTES)
    
    send_invitation_email(invitation_link=invitation_token, invitee_email=invitee_email, inviter_name=inviter_name, inviter_photo_url=inviter_photo_url)

    return InvitationResponse(invitee_email=invitee_email, inviter_email=inviter_email, status=InvitationStatus.PENDING, expires_at=expires_at)


def verify_invitee(db: Session, token: str, invitee_email: EmailStr) -> InvitationResponse:
    invitation = verify_invitation_token(db, token)
    if invitation.invitee_email != invitee_email:
        raise ValueError("Invalid user")
    invitee_email = get_user_by_email(db, invitee_email)
    if not invitee_email:
        raise ValueError("User not found")
    return InvitationResponse(invitee_email=invitee_email, inviter_email=invitation.inviter_email, status=InvitationStatus.PENDING, expires_at=invitation.expires_at)


def verify_invitation_token(db: Session, token: str) -> InvitationTokenPayload:
    decoded_token = decode_invitation_token(token=token) # token payload
    invitation = get_invitation_by_code(db, token)
    if not invitation:
        raise ValueError("Invalid invitation")
    if invitation.status != InvitationStatus.PENDING:
        raise ValueError("Invitation is not pending")
    return decoded_token

# check if pending before accepting in routes layer
def accept_invitation(db: Session, token: str) -> InvitationResponse:
    verification = verify_invitation_token(db, token)
    if not verification:
        raise ValueError("Invalid invitation")
        
    updated_invitation = update_invitation_status(db, token, InvitationStatus.ACCEPTED)
    return InvitationResponse(invitee_email=updated_invitation.invitee_email, inviter_email=get_user(db, updated_invitation.inviter_id).email, status=updated_invitation.status, expires_at=updated_invitation.expires_at)


def decline_invitation(db: Session, invitation_code: str) -> InvitationResponse:
    verification = verify_invitation_token(db, invitation_code)
    if not verification:
        raise ValueError("Invalid invitation")

    updated_invitation = update_invitation_status(db, invitation_code, InvitationStatus.DECLINED)
    return InvitationResponse(invitee_email=updated_invitation.invitee_email, inviter_email=get_user(db, updated_invitation.inviter_id).email, status=updated_invitation.status, expires_at=updated_invitation.expires_at)


def revoke_invitation(db: Session, invitation_code: str) -> InvitationResponse:
    verification = verify_invitation_token(db, invitation_code)
    if not verification:
        raise ValueError("Invalid invitation")
    
    updated_invitation = update_invitation_status(db, invitation_code, InvitationStatus.REVOKED)
    return InvitationResponse(invitee_email=updated_invitation.invitee_email, inviter_email=get_user(db, updated_invitation.inviter_id).email, status=updated_invitation.status, expires_at=updated_invitation.expires_at)


def hash_invitation_code(code: str) -> str:
    pass


def send_invitation_email(invitation_link: str, invitee_email: str, inviter_name: str, inviter_photo_url: Optional[str] = None) -> None:
    pass
