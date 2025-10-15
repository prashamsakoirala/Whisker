from datetime import datetime, timezone
import uuid
from sqlalchemy import DateTime, String, ForeignKey, JSON
from sqlalchemy import Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from typing import List, Optional
from sqlalchemy import Enum as SQLEnum

class Partnerships(Base):
    __tablename__ = "partnerships"

    partnership_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # pull from user table
    partner_1_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    # pull from user table
    partner_2_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    # default time now
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # relationships to User model (assumes user model __tablename__ is 'user')
    partner_1 = relationship("User", foreign_keys=[partner_1_id])
    partner_2 = relationship("User", foreign_keys=[partner_2_id])

class Ownerships(Base):
    __tablename__ = "ownerships"

    partnership_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("partnership.partnership_id"), primary_key=True)
    # TODO implement cat table
    # cat_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cat.cat_id"), nullable=False) primary key is true

    partnership = relationship("Partnership", back_populates="ownerships")
    # relationship to Cat model (assumes cat model __tablename__ is 'cat')
    # cat = relationship("Cat")