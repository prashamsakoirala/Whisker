from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from database import Base
from sqlalchemy.ext.associationproxy import association_proxy


class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(default = "Whiskers")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
    state: Mapped[list['CatState']] = relationship(back_populates='cat')
    inventory: Mapped[list['CatInventory']] = relationship(back_populates='cat')
    animation: Mapped[list['CatAnimation']] = relationship(back_populates='cat')
    partnership: Mapped['Partnership'] = relationship(back_populates='cat')
    active_users = association_proxy('active_cat_association', 'user')

    active_cat_association: Mapped[list['ActiveCat']] = relationship(back_populates='cat')

class CatState(Base):
    __tablename__ = "cat_state"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    hunger: Mapped[int] = mapped_column()
    happiness: Mapped[int] = mapped_column()
    animation: Mapped[str] = mapped_column() # enum
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cat: Mapped['Cat'] = relationship(back_populates='state')

class CatInventory(Base):
    __tablename__ = "cat_inventory"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    fish: Mapped[int] = mapped_column()
    toy: Mapped[int] = mapped_column()
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cat: Mapped['Cat'] = relationship(back_populates='inventory')

class CatMusicPersonality(Base):
    __tablename__ = "cat_music_personality"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    genres: Mapped[CatItemEnum] = mapped_column(primary_key=True)
    artists: Mapped[int] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

class CatAttributeLog(Base):
    __tablename__ = "cat_attribute_log"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), nullable=False, primary_key=True)
    attribute: Mapped[str] = mapped_column() # enum
    value: Mapped[int] = mapped_column()
    action: Mapped[str] = mapped_column() # enum
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cat: Mapped['Cat'] = relationship(back_populates='attribute_logs')