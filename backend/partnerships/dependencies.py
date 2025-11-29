from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from .crud import get_all_partnerships_for_user
from users.models import User
from users.dependencies import get_current_user

async def get_current_user_partnerships(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    partnerships = get_all_partnerships_for_user(db, current_user.user_id)
    return partnerships