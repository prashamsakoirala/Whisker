from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional
import uuid
from datetime import datetime
from typing import List
from .types import Provider, AuthorizationStatus, RegistrationStatus

class UserBase(BaseModel):
    name: Annotated[str, Field(description="User's name")]
    email: Annotated[EmailStr, Field(description="User's email")]
    profile_picture: Annotated[Optional[str], Field(default=None, description="Profile picture URL")] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]
    created_at: Annotated[datetime, Field(description="Creation timestamp")]

    class Config:
        from_attributes = True


class UserRegistrationBase(BaseModel):
    status: Annotated[RegistrationStatus, Field(default=RegistrationStatus.SIGNED_IN, description="Registration status")]


class UserRegistrationUpdate(UserRegistrationBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]


class UserRegistrationCreate(UserRegistrationBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]


class UserRegistrationResponse(UserRegistrationBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]
    updated_at: Annotated[datetime, Field(description="Last updated timestamp")]

    class Config:
        from_attributes = True

# TODO change expires at to datetimenow + duration in seconds maybe 1 week or so...
class UserAuthorizationBase(BaseModel):
    provider: Annotated[Provider, Field(description="Authorization provider")]
    refresh_token: Annotated[Optional[str], Field(default=None, description="Refresh token")]
    expires_at: Annotated[Optional[datetime], Field(default=None, description="Expiration datetime")]
    status: Annotated[AuthorizationStatus, Field(default=AuthorizationStatus.MISSING, description="Authorization/token status")]


class UserAuthorizationCreate(UserAuthorizationBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]


class UserAuthorizationUpdate(UserAuthorizationBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]


class UserAuthorizationResponse(UserAuthorizationBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]
    updated_at: Annotated[datetime, Field(description="Last updated timestamp")]

    class Config:
        from_attributes = True


class UserMusicPersonalityBase(BaseModel):
    genres: Annotated[Optional[List[str]], Field(default=None, description="Favorite genres")]
    artists: Annotated[Optional[List[str]], Field(default=None, description="Favorite artists")]


class UserMusicPersonalityCreate(UserMusicPersonalityBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]


class UserMusicPersonalityResponse(UserMusicPersonalityBase):
    user_id: Annotated[uuid.UUID, Field(description="User's unique ID")]
    updated_at: Annotated[datetime, Field(description="Last updated timestamp")]

    class Config:
        from_attributes = True

