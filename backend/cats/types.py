from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from database import Base
from sqlalchemy.ext.associationproxy import association_proxy

class CatAnimationEnum(str, Enum):
    IDLE = "idle"
    SLEEP = "sleep"

class CatEventEnum(str, Enum):
    FEED = "feed"
    PLAY = "play"