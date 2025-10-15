from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth.google.oauth import oauth
from backend.users.schemas import UserAuthorizationCreate
from database import get_db
from starlette.requests import Request
from users.crud import get_user_by_email, create_user, get_user_registration, create_user_registration
from users.models import User
from users.types import Provider, AuthorizationStatus
from auth.tokens import create_access_token, create_refresh_token, hash_token
from users.services import add_user_authorization_token
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
    refresh_token = token.get("refresh_token")
    expires_at = token.get("expires_at")
    hashed_refresh_token = hash_token(refresh_token)

    # TODO get token for google, store it + add it to current database but hashed
    user_info = token.get('userinfo')
    if not user_info: # if userinfo not in token, fetch it
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo', token=token)
        user_info = resp.json()
    
    # create new user with user_info it it does not exist in DB
    user = get_user_by_email(db, email=user_info['email'])
    if not user:
        new_user = create_user(db, user_info.get('name'), user_info.get('email'), user_info.get('picture'))
        create_user_registration(db, new_user.id) # create registration entry for new user
        add_user_authorization_token(db, token=UserAuthorizationCreate(user_id=new_user.id, provider=Provider.GOOGLE, refresh_token=hashed_refresh_token, expires_at=expires_at, status=AuthorizationStatus.ACTIVE))
        redirect_url = "/onboarding"
    else:
        add_user_authorization_token(db, token=UserAuthorizationCreate(user_id=user.id, provider=Provider.GOOGLE, refresh_token=hashed_refresh_token, expires_at=expires_at, status=AuthorizationStatus.ACTIVE))
        redirect_url = "/home"

    access_token = create_access_token(TokenPayload(user_id=str(user.id), scope=TokenScope.ACCESS.value))
    refresh_token = create_refresh_token(TokenPayload(user_id=str(user.id), scope=TokenScope.REFRESH.value))
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax")

    # TODO figure out how to redirect URL to corresponding correct page
    return RedirectResponse(url=redirect_url)