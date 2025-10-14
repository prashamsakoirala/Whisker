from datetime import datetime, timezone
from sqlalchemy import  ForeignKey, text, DateTime, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from database import Base
from sqlalchemy.ext.associationproxy import association_proxy


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    picture: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    active_cat = association_proxy('active_cat_association', 'cat')
    
    primary_partnership: Mapped['Partnership'] = relationship(back_populates='primary_user', foreign_keys='Partnership.primary_user_id')
    secondary_partnership: Mapped['Partnership'] = relationship(back_populates='secondary_user', foreign_keys='Partnership.secondary_user_id')
    active_cat_association: Mapped['ActiveCat'] = relationship(back_populates='user')

class ActiveCat(Base):
    __tablename__ = "active_cat"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), nullable=False)

    user: Mapped['User'] = relationship(back_populates='active_cat_association')
    cat: Mapped['Cat'] = relationship(back_populates='active_cat_association')

class Partnership(Base):
    __tablename__ = "partnerships"

    partnership_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    primary_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    primary_user: Mapped['User'] = relationship(back_populates='primary_partnership', foreign_keys=[primary_user_id])

    secondary_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    secondary_user: Mapped['User'] = relationship(back_populates='secondary_partnership', foreign_keys=[secondary_user_id])

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), nullable=True)
    cat: Mapped['Cat'] = relationship(back_populates='partnership')