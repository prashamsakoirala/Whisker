from datetime import datetime, timezone
import uuid
from sqlalchemy import DateTime, String, ForeignKey, JSON
from sqlalchemy import Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from typing import List, Optional
from sqlalchemy import Enum as SQLEnum
from .types import InvitationStatus

class Invitations(Base):
    __tablename__ = "invitations"

    invitation_code: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, primary_key=True)
    inviter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    invitee_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    invitee_email: Mapped[Optional[str]] = mapped_column(unique=True, nullable=False)
    status: Mapped[InvitationStatus] = mapped_column(SQLEnum(InvitationStatus), nullable=False, default=InvitationStatus.PENDING)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
