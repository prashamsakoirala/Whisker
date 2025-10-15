from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .schemas import UserResponse, UserRegistrationResponse
from .dependencies import get_current_user
from .services import get_registration_status
from .models import User

router = APIRouter(prefix="/users", tags=["users"])

# GET /users/me/
@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# GET /users/me/registration
@router.get("/me/registration", response_model=UserRegistrationResponse)
async def read_user_registration(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        registration = get_registration_status(db, current_user.user_id)
        return registration
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# GET /users/me/cats # gets all the user's cats

# GET /users/me/cats/{cat_id}/partner # gets partner for a specific cat



# GET /users/all # admin only, gets all users
    ## Need crud for all users
# GET /users/{user_id} # admin only, gets specific user
# DELETE /users/{user_id} # admin only, deletes specific user
# PATCH /users/{user_id} # admin only, updates specific user
# GET /users/{user_id}/cats # admin only, gets all the user's cats
# GET /users/{user_id}/cats/{cat_id}/partner # admin only, gets partner for a specific cat