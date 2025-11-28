from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from database import Base
from sqlalchemy.ext.associationproxy import association_proxy
from .types import CatItemEnum, CatStateEnum

class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(default = "Whiskers")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    ownership = relationship("Ownerships", back_populates="cat")

class CatState(Base):
    __tablename__ = "cat_state"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    attribute: Mapped[CatStateEnum] = mapped_column(primary_key=True)
    # add ranges to this?
    value: Mapped[int] = mapped_column()
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

class CatInventory(Base):
    __tablename__ = "cat_inventory"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    inventory: Mapped[CatItemEnum] = mapped_column(primary_key=True)
    # add ranges to this?
    value: Mapped[int] = mapped_column()
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

# class CatMusicPersonality(Base):
#     __tablename__ = "cat_music_personality"

#     cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
#     genres: Mapped[CatItemEnum] = mapped_column(primary_key=True)
#     updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
