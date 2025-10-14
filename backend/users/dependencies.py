from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
import jwt
from jwt import PyJWTError
from database import get_db
from models.user_model import User, Partnership
from models.cat_model import *
from auth.config import SECRET_KEY, ALGORITHM
from auth.tokens import create_access_token
from schemas.token_schema import *

# get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None or payload.get("scope") != "access_token":
            raise HTTPException(status_code=401, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # TODO use crud operations for the following instead of direct database access
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user