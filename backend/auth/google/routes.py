from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from auth.google.oauth import oauth
from database import get_db
from starlette.requests import Request
from users.crud import get_user_by_email, create_user, get_user_registration, create_user_registration
from users.models import User
from auth.tokens import create_access_token, create_refresh_token
from auth.schemas import Token, TokenPayload
from auth.types import TokenScope

router = APIRouter(prefix="/auth/google", tags=["auth"])

@router.get("/login") #added start, should be fine
async def get_google_auth(request: Request):
    redirect_uri = request.url_for('auth.google.callback')
    # await and return the response
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    return response

@router.get("/callback", name="auth.google.callback")
async def get_google_auth_callback(request: Request, response: Response, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    
    user_info = token.get('userinfo')
    if not user_info: # if userinfo not in token, fetch it
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo', token=token)
        user_info = resp.json()
    
    # create new user with user_info it it does not exist in DB
    user = get_user_by_email(db, email=user_info['email'])
    if not user:
        user = create_user(db, user_info.get('name'), user_info.get('email'), user_info.get('picture'))
        create_user_registration(db, user.id) # create registration entry for new user
        
    access_token = create_access_token(TokenPayload(user_id=str(user.id), scope=TokenScope.ACCESS.value))
    refresh_token = create_refresh_token(TokenPayload(user_id=str(user.id), scope=TokenScope.REFRESH.value))

    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax")

    return {"message": "Login successful"}

# from fastapi import APIRouter, Depends
# from fastapi.responses import RedirectResponse
# from sqlalchemy.orm import Session
# from auth.dependencies import refresh_access_token
# from database import get_db

# router = APIRouter(prefix="/auth", tags=["auth"])

# @router.get("/google/start") #added start, should be fine
# async def get_google_auth():
#     auth_url = get_google_auth_url()
#     return RedirectResponse(url=auth_url)

# @router.get("/google/callback")
# async def google_callback(code: str, db: Session = Depends(get_db)):
#     token = await get_google_auth_callback(code, db)
#     return token

# @router.post("/refresh")
# async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
#     return await refresh_access_token(refresh_token, db)
        