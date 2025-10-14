from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional
import uuid
from datetime import datetime
from models.user_model import *
import enum
from typing import List

class Provider(str, enum.Enum):
    GOOGLE = "google"
    SPOTIFY = "spotify"

class Access(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class AuthorizationStatus(str, enum.Enum):
    ACTIVE = "active"           # token is present and usable
    EXPIRED = "expired"         # token expired and needs refresh
    REVOKED = "revoked"         # token was revoked by user/provider
    MISSING = "missing"         # no token stored

class RegistrationStatus(str, enum.Enum):
    SIGNED_IN = "signed_in"                # user signed in with Google
    INVITATION_SENT = "invitation_sent"    # user entered partner's email
    INVITATION_ACCEPTED = "invitation_accepted"    # waiting for partner acceptance
    NAMED_PET = "named_pet"                # pet named
    SPOTIFY_LINKED = "spotify_linked"      # spotify linked (per user)
    PERSONALITY_GENERATED = "personality_generated"  # personality generated
    COMPLETE = "complete"