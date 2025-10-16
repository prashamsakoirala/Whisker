from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from users.dependencies import get_current_user
from users.models import User
from .services import generate_and_send_invitation, get_invitation_information, accept_invitation, revoke_invitation
from .schemas import InvitationCreate, InvitationResponse, InvitationDisplay

router = APIRouter(prefix="/invitations", tags=["invitations"])

@router.post("/send", response_model=InvitationResponse)
async def send_invitation(invitee_email: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inviter_email = current_user.email
    return generate_and_send_invitation(db=db, invitation_data=InvitationCreate(invitee_email=invitee_email, inviter_email=inviter_email))

# GET /invitations/ (depends database, get current user, invitation code)
# need to implement get endpoint
# get should be the current user is the invitee
@router.get("/", response_model=InvitationDisplay)
async def retrieve_invitation_code(code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    invitee_email = current_user.email
    # need get the invitation should have the partner name, partner image
    # need to add http errors?
    return get_invitation_information(db=db, invitation_code=code, verifier_email=invitee_email)

# POST /invitations/accept (depends database, get current user, invitation code)
@router.post("/accept", response_model=InvitationResponse)
async def user_accept_invitation(code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # return new partnership as well once this is accepted
    # TODO create new partnership in partnership service as a result of this posting
    return accept_invitation(db=db, token=code, acceptor_email=current_user.email)

# PATCH /invitations/revoke (revoking invitation)(depends database, get current user has to equal inviter, invitation code)
@router.patch("/revoke", response_model=InvitationResponse)
async def user_revoke_invitation(code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return revoke_invitation(db=db, invitation_code=code, inviter_email=current_user.email)
