from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from datetime import datetime, timezone, timedelta
from .models import Invitations
from .types import InvitationStatus
from config import INVITATION_TOKEN_EXPIRE_MINUTES
from users.crud import get_user_by_email


def create_invitation(db: Session, inviter_id: uuid.UUID, invitee_email: str, invitation_code: Optional[str] = None, expires_in_minutes: int = INVITATION_TOKEN_EXPIRE_MINUTES) -> Invitations:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
    invitation = Invitations(invitation_code=invitation_code, inviter_id=inviter_id, invitee_email=invitee_email, expires_at=expires_at, status=InvitationStatus.PENDING)
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation

def get_invitation_by_code(db: Session, invitation_code: str) -> Optional[Invitations]:
    return db.query(Invitations).filter(Invitations.invitation_code == invitation_code).first()

def get_all_invitations_by_inviter_email(db: Session, inviter_email: str) -> List[Invitations]:
    inviter_id = get_user_by_email(db, inviter_email).user_id
    return db.query(Invitations).filter(Invitations.inviter_id == inviter_id).all()

def get_all_invitations_by_invitee_email(db: Session, invitee_email: str) -> List[Invitations]:
    return db.query(Invitations).filter(Invitations.invitee_email == invitee_email).all()

def get_all_invitations_by_both_emails(db: Session, invitee_email: str, inviter_email: str) -> Optional[Invitations]:
    inviter_id = get_user_by_email(db, inviter_email).user_id
    return db.query(Invitations).filter(Invitations.invitee_email == invitee_email, Invitations.inviter_id == inviter_id).all()

def get_most_recent_invitation_by_emails(db: Session, invitee_email: str, inviter_email: str) -> Optional[Invitations]:
    inviter_id = get_user_by_email(db, inviter_email).user_id
    return db.query(Invitations).filter(Invitations.invitee_email == invitee_email, Invitations.inviter_id == inviter_id).order_by(Invitations.sent_at.desc()).first()

def get_most_recent_invitation_for_invitee(db: Session, invitee_email: str) -> Optional[Invitations]:
    return db.query(Invitations).filter(Invitations.invitee_email == invitee_email).order_by(Invitations.sent_at.desc()).first()


def get_invitation_by_id(db: Session, invitation_id: uuid.UUID) -> Optional[Invitations]:
    return db.query(Invitations).filter(Invitations.id == invitation_id).first()


def get_invitations_by_inviter(db: Session, inviter_id: uuid.UUID) -> List[Invitations]:
    return db.query(Invitations).filter(Invitations.inviter_id == inviter_id).all()


def get_invitations_by_invitee(db: Session, invitee_id: uuid.UUID) -> List[Invitations]:
    return db.query(Invitations).filter(Invitations.invitee_id == invitee_id).all()


def get_pending_invitations(db: Session, invitee_email: str) -> List[Invitations]:
    return db.query(Invitations).filter(Invitations.invitee_email == invitee_email, Invitations.status == InvitationStatus.PENDING).order_by(Invitations.sent_at.desc()).all()


def update_invitation_status(db: Session, invitation_code: str, status: InvitationStatus, invitee_id: Optional[uuid.UUID] = None) -> Optional[Invitations]:
    invitation = get_invitation_by_code(db, invitation_code)
    if not invitation:
        return None
    
    invitation.status = status
    invitation.updated_at = datetime.now(timezone.utc)
    
    if invitee_id is not None:
        invitation.invitee_id = invitee_id
    
    db.commit()
    db.refresh(invitation)
    return invitation


def update_invitation(db: Session, invitation_code: str, status: Optional[InvitationStatus] = None, invitee_id: Optional[uuid.UUID] = None, invitee_email: Optional[str] = None, expires_at: Optional[datetime] = None) -> Optional[Invitations]:
    invitation = get_invitation_by_code(db, invitation_code)
    if not invitation:
        return None
    
    if status is not None:
        invitation.status = status
    if invitee_id is not None:
        invitation.invitee_id = invitee_id
    if invitee_email is not None:
        invitation.invitee_email = invitee_email
    if expires_at is not None:
        invitation.expires_at = expires_at
    
    invitation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(invitation)
    return invitation


def revoke_invitation(db: Session, invitation_code: str) -> Optional[Invitations]:
    invitation = get_invitation_by_code(db, invitation_code)
    if not invitation:
        return None
    
    invitation.status = InvitationStatus.DECLINED
    invitation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(invitation)
    return invitation


def delete_invitation(db: Session, invitation_code: str) -> bool:
    invitation = get_invitation_by_code(db, invitation_code)
    if not invitation:
        return False
    
    db.delete(invitation)
    db.commit()
    return True


def expire_old_invitations(db: Session) -> int:
    now = datetime.now(timezone.utc)
    expired_invitations = db.query(Invitations).filter(Invitations.expires_at < now, Invitations.status == InvitationStatus.PENDING).all()

    count = 0
    for invitation in expired_invitations:
        invitation.status = InvitationStatus.EXPIRED
        invitation.updated_at = now
        count += 1
    
    db.commit()
    return count


def is_invitation_valid(db: Session, invitation_code: str) -> bool:
    invitation = get_invitation_by_code(db, invitation_code)
    if not invitation:
        return False
    
    if invitation.status != InvitationStatus.PENDING:
        return False
    
    if invitation.expires_at < datetime.now(timezone.utc):
        invitation.status = InvitationStatus.EXPIRED
        invitation.updated_at = datetime.now(timezone.utc)
        db.commit()
        return False
    
    return True
