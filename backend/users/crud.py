from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from datetime import datetime
from .models import User, UserRegistration, UserAuthorization, UserMusicPersonality
from .types import Provider, AuthorizationStatus, RegistrationStatus

def create_user(db: Session, name: str, email: str, profile_picture: Optional[str] = None) -> User:
	user = User(name=name, email=email, profile_picture=profile_picture)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user

def get_user(db: Session, user_id: uuid.UUID) -> Optional[User]:
	return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
	return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: uuid.UUID, name: Optional[str] = None, email: Optional[str] = None, profile_picture: Optional[str] = None) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if profile_picture is not None:
        user.profile_picture = profile_picture
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: uuid.UUID) -> bool:
	user = get_user(db, user_id)
	if not user:
		return False
	db.delete(user)
	db.commit()
	return True


def create_user_registration(db: Session, user_id: uuid.UUID, status: RegistrationStatus = RegistrationStatus.SIGNED_IN) -> UserRegistration:
	existing = get_user_registration(db, user_id)
	if existing:
		return existing
	reg = UserRegistration(user_id=user_id, status=status)
	db.add(reg)
	db.commit()
	db.refresh(reg)
	return reg


def get_user_registration(db: Session, user_id: uuid.UUID) -> Optional[UserRegistration]:
	return db.query(UserRegistration).filter(UserRegistration.user_id == user_id).first()

def update_user_registration(db: Session, user_id: uuid.UUID, status: Optional[RegistrationStatus] = None) -> Optional[UserRegistration]:
	reg = get_user_registration(db, user_id)
	if not reg:
		return None
	if status is not None:
		reg.status = status
	reg.updated_at = datetime.now()
	db.commit()
	db.refresh(reg)
	return reg

def delete_user_registration(db: Session, user_id: uuid.UUID) -> bool:
	reg = get_user_registration(db, user_id)
	if not reg:
		return False
	db.delete(reg)
	db.commit()
	return True

def create_user_authorization(db: Session, user_id: uuid.UUID, provider: Provider, refresh_token: Optional[str] = None, expires_at: Optional[datetime] = None, status: AuthorizationStatus = AuthorizationStatus.MISSING) -> UserAuthorization:
	existing = db.query(UserAuthorization).filter(UserAuthorization.user_id == user_id, UserAuthorization.provider == provider).first()
	if existing:
		existing.refresh_token = refresh_token
		existing.expires_at = expires_at
		existing.status = status
		existing.updated_at = datetime.now()
		db.commit()
		db.refresh(existing)
		return existing
	auth = UserAuthorization(user_id=user_id, provider=provider, refresh_token=refresh_token, expires_at=expires_at, status=status)
	db.add(auth)
	db.commit()
	db.refresh(auth)
	return auth


def get_user_authorization(db: Session, user_id: uuid.UUID) -> List[UserAuthorization]:
	return db.query(UserAuthorization).filter(UserAuthorization.user_id == user_id).all()


def update_user_authorization(db: Session, user_id: uuid.UUID, refresh_token: Optional[str] = None, expires_at: Optional[datetime] = None, status: Optional[AuthorizationStatus] = None) -> Optional[UserAuthorization]:
	auth = get_user_authorization(db, user_id)
	if not auth:
		return None
	if refresh_token is not None:
		auth.refresh_token = refresh_token
	if expires_at is not None:
		auth.expires_at = expires_at
	if status is not None:
		auth.status = status
	auth.updated_at = datetime.now()
	db.commit()
	db.refresh(auth)
	return auth


def delete_user_authorization(db: Session, authorization_id: uuid.UUID) -> bool:
	auth = get_user_authorization(db, authorization_id)
	if not auth:
		return False
	db.delete(auth)
	db.commit()
	return True


def create_user_music_personality(db: Session, user_id: uuid.UUID, genres: Optional[List[str]] = None, artists: Optional[List[str]] = None) -> UserMusicPersonality:
	existing = get_user_music_personality(db, user_id)
	if existing:
		return existing
	mp = UserMusicPersonality(user_id=user_id, genres=genres, artists=artists)
	db.add(mp)
	db.commit()
	db.refresh(mp)
	return mp


def get_user_music_personality(db: Session, user_id: uuid.UUID) -> Optional[UserMusicPersonality]:
	return db.query(UserMusicPersonality).filter(UserMusicPersonality.user_id == user_id).first()


def update_user_music_personality(db: Session, user_id: uuid.UUID, genres: Optional[List[str]] = None, artists: Optional[List[str]] = None) -> Optional[UserMusicPersonality]:
	mp = get_user_music_personality(db, user_id)
	if not mp:
		return None
	if genres is not None:
		mp.genres = genres
	if artists is not None:
		mp.artists = artists
	mp.updated_at = datetime.now()
	db.commit()
	db.refresh(mp)
	return mp


def delete_user_music_personality(db: Session, user_id: uuid.UUID) -> bool:
	mp = get_user_music_personality(db, user_id)
	if not mp:
		return False
	db.delete(mp)
	db.commit()
	return True

