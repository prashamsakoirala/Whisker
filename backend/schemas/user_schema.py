from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
import uuid
from models.user_model import *

class UserRead(BaseModel):
    id: Annotated[uuid.UUID, Field(description="User's unique ID")]
    name: Annotated[str, Field(description="User's name")]
    email: Annotated[EmailStr, Field(description="User's unique ID")]
    picture: Annotated[str, Field(description="Picture url to profile image")]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: Annotated[str, Field(description="User's name")]
    email: Annotated[EmailStr, Field(description="User's unique ID")]
    picture: Annotated[str, Field(description="Picture url to profile image")]
    
    class Config:
        from_attributes = True

class PartnershipRead(BaseModel):
    partnership_id: Annotated[uuid.UUID, Field(description="User's unique ID")]
    primary_user_id: Annotated[uuid.UUID, Field(description="Primary user's ID")]
    secondary_user_id: Annotated[uuid.UUID, Field(description="Secondary user's ID")]

    class Config:
        from_attributes = True

class PartnershipCreate(BaseModel):
    primary_user_id: Annotated[uuid.UUID, Field(description="Primary user's ID")]
    secondary_user_id: Annotated[uuid.UUID, Field(description="Secondary user's ID")]
    
    class Config:
        from_attributes = True
