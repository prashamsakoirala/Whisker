from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, List
import uuid
from models.cat_model import CatStateEnum, CatItemEnum, CatAnimationEnum

# class CatStateRead(BaseModel):
#     state : Annotated[CatStateEnum, Field(description="State of interest")]
#     value : Annotated[int, Field(description="Value of state")]
#     last_updated : Annotated[datetime, Field(description="Timestamp when state was last updated")]

#     class Config:
#         from_attributes = True

# class CatInventoryRead(BaseModel):
#     item : Annotated[CatItemEnum, Field(description="Item of interest")]
#     value : Annotated[int, Field(description="Number of inventory items")]
#     last_updated : Annotated[datetime, Field(description="Timestamp when item was last updated")]
    
#     class Config:
#         from_attributes = True

# class CatAnimationRead(BaseModel):
#     animation : Annotated[CatAnimationEnum, Field(description="Current cat animation")]
#     last_updated : Annotated[datetime, Field(description="Timestamp when animation was last updated")]
    
#     class Config:
#         from_attributes = True

# class CatCreate(BaseModel):
#     name: Annotated[str, Field(description="Name of the cat", default="Whiskers")]

# class CatRead(BaseModel):
#     id: Annotated[uuid.UUID, Field(description="Cat's unique ID")]
#     name: Annotated[str, Field(description="Name of the cat")]
#     created_at: Annotated[datetime, Field(description="Timestamp when cat was created")]
#     state: List[CatStateRead] = Field(default=[], description="List of cat states")
#     inventory: List[CatInventoryRead] = Field(default=[], description="List of inventory items")
#     animation: List[CatAnimationRead] = Field(None, description="Current cat animation")

#     class Config:
#         from_attributes = True
