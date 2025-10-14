from pydantic import BaseModel, Field
from typing import Annotated
from models.user_model import *

class Token(BaseModel):
    access_token: Annotated[str, Field()]
    refresh_token: Annotated[str, Field()]
    token_type: Annotated[str, Field(default="bearer")]

class TokenPayload(BaseModel):
    sub: Annotated[str, Field()]