from datetime import datetime, timezone
import uuid
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class Partnerships(Base):
    __tablename__ = "partnerships"

    partnership_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # pull from user table
    partner_1_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    # pull from user table
    partner_2_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    # default time now
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # relationships to User model (assumes user model __tablename__ is 'user')
    partner_1 = relationship("User", foreign_keys=[partner_1_id])
    partner_2 = relationship("User", foreign_keys=[partner_2_id])
    
    # relationship to Ownerships
    ownerships = relationship("Ownerships", back_populates="partnership")