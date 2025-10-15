from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth.google.oauth import oauth
from backend.users.routes import get_current_user
from database import get_db
from starlette.requests import Request
from users.crud import get_user_by_email, create_user, get_user_registration, create_user_registration
from users.models import User
from auth.tokens import create_access_token, create_refresh_token, decode_token
from auth.schemas import Token, TokenPayload
from auth.types import TokenScope

router = APIRouter(prefix="/auth", tags=["auth"])

# Refresh access token, need to pass in a access token, then if expired then
# get refresh token from cookie, verify it, then create new access token (ie by verify i mean decode the refresh token)
# if decoded refresh token is an actual token then good
# otherwise if not then error and not correct refresh token or expired refresh token
# if not correct refresh token then 401 error
# if expired refresh token then 403 error and give the user a message to login again

# wait wouldnt you use the refresh token to get a new access token???
# yes you would, so you would need to get the refresh token from the cookie
# then decode the refresh token, if valid then create new access token
# if not valid then error

# then you redirect user back to home page if they are refreshed/verified

@router.post("/refresh", response_model=Token)
async def refresh_access_token(response: Response, refresh_token: str = Cookie(str)):
    # Create new access token
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(TokenPayload(user_id=str(payload["user_id"]), scope=TokenScope.ACCESS.value))
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
    
    return RedirectResponse(url="/home")

