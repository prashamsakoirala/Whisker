from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from database import Base
from sqlalchemy.ext.associationproxy import association_proxy

from .user_model import Partnership, ActiveCat

class CatAnimationEnum(str, Enum):
    IDLE = "idle"
    SLEEP = "sleep"

class CatEventEnum(str, Enum):
    FEED = "feed"
    PLAY = "play"

class CatStateEnum(str, Enum):
    HUNGER = "hunger"
    HAPPINESS = "happiness"

class CatItemEnum(str, Enum):
    FISH = "fish"
    TOY = "toy"

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
    state: Mapped[CatStateEnum] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cat: Mapped['Cat'] = relationship(back_populates='state')

class CatInventory(Base):
    __tablename__ = "cat_inventory"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    item: Mapped[CatItemEnum] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cat: Mapped['Cat'] = relationship(back_populates='inventory')

class CatAnimation(Base):
    __tablename__ = "cat_animation"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    animation: Mapped[CatAnimationEnum] = mapped_column()
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cat: Mapped['Cat'] = relationship(back_populates='animation')