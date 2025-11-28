from pydantic import BaseModel, Field
from typing import Annotated, Optional
import uuid
from datetime import datetime


class PartnershipBase(BaseModel):
	partner_1_id: Annotated[uuid.UUID, Field(description="Partner 1 user id")]
	partner_2_id: Annotated[uuid.UUID, Field(description="Partner 2 user id")]


class PartnershipCreate(PartnershipBase):
	pass


class PartnershipResponse(PartnershipBase):
	partnership_id: Annotated[uuid.UUID, Field(description="Partnership unique id")]
	created_at: Annotated[datetime, Field(description="Creation timestamp")]

	class Config:
		from_attributes = True