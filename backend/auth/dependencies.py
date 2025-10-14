from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
import jwt
from jwt import PyJWTError
from database import get_db
from models.user_model import User, Partnership
from models.cat_model import *
from .config import SECRET_KEY, ALGORITHM
from .tokens import create_access_token
from schemas.token_schema import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None or payload.get("scope") != "access_token":
            raise HTTPException(status_code=401, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_partnership(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    partnership = db.query(Partnership).filter(or_(Partnership.primary_user_id == current_user.id, Partnership.secondary_user_id == current_user.id)
    ).first()
    if not partnership:
        raise HTTPException(status_code=404, detail="Partnership not found")
    return partnership


async def get_current_cat(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter(Cat.id == current_user.active_cat).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    return cat


# if refresh token is expired, get another refresh token
# this would have to be initiated by the frontend
# redo oauth flow
async def refresh_access_token(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")

    # check if refresh token is expired

    if user_id is None or payload.get("scope") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    existing_user_id = db.query(User).filter(User.id == user_id).first()
    if not existing_user_id:
        raise HTTPException(status_code=401, detail="User not found")

    access_token_jwt = create_access_token(data={"sub": existing_user_id.id})
    return Token(
        access_token=access_token_jwt,
        refresh_token=refresh_token,
        token_type="bearer",
    )   

