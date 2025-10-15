from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_current_user
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserResponse, UserRegistrationResponse

router = APIRouter(prefix="/users", tags=["users"])

# GET /users/me/
@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    # Check for value errors in the dependency and raise corresponding HTTP exceptions
    return UserResponse(from_orm=current_user)

# GET /users/me/registration
@router.get("/me/registration", response_model=UserRegistrationResponse)
async def get_user_registration(current_user: User = Depends(get_current_user)):
    registration = get_user_registration(current_user.id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    return UserRegistrationResponse(from_orm=registration)

# GET /users/me/cats # gets all the user's cats

# GET /users/me/cats/{cat_id}/partner # gets partner for a specific cat



# GET /users/all # admin only, gets all users
    ## Need crud for all users
# GET /users/{user_id} # admin only, gets specific user
# DELETE /users/{user_id} # admin only, deletes specific user
# PATCH /users/{user_id} # admin only, updates specific user
# GET /users/{user_id}/cats # admin only, gets all the user's cats
# GET /users/{user_id}/cats/{cat_id}/partner # admin only, gets partner for a specific cat


# from fastapi import APIRouter, Depends, HTTPException
# from auth.dependencies import get_current_user
# from models.user_model import User, Partnership
# from sqlalchemy.orm import Session
# from database import get_db

# router = APIRouter(prefix="/users", tags=["users"])

# @router.get("/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

# # Wouldn't it make more sense to initalize a partnership when you have the other user's id?

# @router.post("/me/partnership", response_model=dict)
# async def init_partnership(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if current_user.primary_partnership:
#         raise HTTPException(status_code=403, detail="Partnership already exists")

#     partnership = Partnership(primary_user=current_user)
#     db.add(partnership)
#     db.commit()
#     db.refresh(partnership)

#     return {
#         "message": "Partnership initialized",
#         "partnership_id": str(partnership.partnership_id),
#         "primary_user_id": str(partnership.primary_user_id),
#     }

# # join_partnership(primary_user, current_user=Depends(get_current_user()))