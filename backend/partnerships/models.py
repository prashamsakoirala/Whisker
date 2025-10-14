from datetime import datetime, timezone
import uuid
from sqlalchemy import DateTime, String, ForeignKey, JSON
from sqlalchemy import Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from typing import List, Optional
from sqlalchemy import Enum as SQLEnum

class Partnership(Base):
	__tablename__ = "partnership"

	partnership_id: 
	# pull from user table
	partner_1_id: 
	# pull from user table
	partner_2_id: 
	# default time now
	created_at: 
	
class Ownership(Base):
	__tablename__ = "ownership"

    # pull from previous table, primary key
    partnership_id:
    # TODO implement cat table
    cat_id: