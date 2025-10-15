from pydantic import BaseModel, Field
from typing import Annotated

class Token(BaseModel):
    access_token: Annotated[str, Field()]
    token_type: Annotated[str, Field(default="bearer")]

class TokenData(BaseModel):
    user_id: Annotated[str, Field()]
    exp: Annotated[int, Field()]
    scope: Annotated[str, Field()]  # helpful for distinguishing access vs refresh

# Payload model used for encoding/decoding tokens
class TokenPayload(BaseModel):
    user_id: str
    scope: str