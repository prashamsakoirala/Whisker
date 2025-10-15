from datetime import datetime, timezone
import uuid
from sqlalchemy import DateTime, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from typing import List, Optional
from sqlalchemy import Enum as SQLEnum
from .types import Provider, Access, AuthorizationStatus, RegistrationStatus

class User(Base):
	__tablename__ = "users"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	status: Mapped[Access] = mapped_column(SQLEnum(Access, name="access"), nullable=False, default=Access.USER)
	profile_picture: Mapped[Optional[str]] = mapped_column(String, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

	registrations: Mapped[List['UserRegistration']] = relationship(back_populates='user', cascade='all, delete-orphan')
	authorizations: Mapped[List['UserAuthorization']] = relationship(back_populates='user', cascade='all, delete-orphan')
	music_personality: Mapped[Optional['UserMusicPersonality']] = relationship(back_populates='user', uselist=False, cascade='all, delete-orphan')


class UserRegistration(Base):
	__tablename__ = "user_registrations"

	user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
	status: Mapped[RegistrationStatus] = mapped_column(SQLEnum(RegistrationStatus, name="registration_status"), nullable=False, default=RegistrationStatus.SIGNED_IN)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

	user: Mapped['User'] = relationship(back_populates='registrations')


class UserAuthorization(Base):
	__tablename__ = "user_authorizations"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
	user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
	provider: Mapped[Provider] = mapped_column(SQLEnum(Provider, name="provider"), nullable=False)
	refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
	expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
	status: Mapped[AuthorizationStatus] = mapped_column(SQLEnum(AuthorizationStatus, name="authorization_status"), nullable=False, default=AuthorizationStatus.MISSING)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

	user: Mapped['User'] = relationship(back_populates='authorizations')

# Don't deal with this until we get to Spotify integration
class UserMusicPersonality(Base):
	__tablename__ = "user_music_personality"

	user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
	genres: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
	artists: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

	user: Mapped['User'] = relationship(back_populates='music_personality')
