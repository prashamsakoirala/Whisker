from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional
import uuid
from datetime import datetime
from typing import List
from .types import InvitationStatus

class InvitationBase(BaseModel):
    invitee_email: EmailStr
    inviter_email: EmailStr

class InvitationCreate(InvitationBase):
    pass

class InvitationTokenPayload(InvitationBase):
    pass

class InvitationTokenDecoded(InvitationBase):
    expires_at: datetime

class InvitationResponse(InvitationBase):
    status: InvitationStatus
    expires_at: datetime
