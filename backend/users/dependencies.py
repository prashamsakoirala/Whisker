from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt import PyJWTError
from database import get_db
from auth.config import SECRET_KEY, ALGORITHM
from users.crud import get_user

# get_current_user
# What does the following do?

# Checks to make sure that there is an Authorization header with a valid JWT token in the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Get payload from token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Get User ID from payload
        user_id = payload.get("sub")
        # If user_id is None
        if user_id is None:
            raise ValueError("Invalid token: missing user ID")

        # If scope is not access_token
        if payload.get("scope") != "access_token":
            raise ValueError("Invalid token: incorrect scope")
        
    except PyJWTError:
        raise ValueError("Invalid token")

    # TODO use crud operations for the following instead of direct database access
    user = get_user(db = db, user_id=user_id)
    if not user:
        raise ValueError("User not found")
    return user