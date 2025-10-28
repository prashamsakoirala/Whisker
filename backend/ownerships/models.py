from datetime import datetime, timezone
import uuid
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class Ownerships(Base):
    __tablename__ = "ownerships"

    partnership_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("partnerships.partnership_id"), primary_key=True)
    cat_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cats.id"), primary_key=True)

    # Use string literals to avoid circular imports
    partnership = relationship("Partnerships", back_populates="ownerships")
    cat = relationship("Cat", back_populates="ownership")