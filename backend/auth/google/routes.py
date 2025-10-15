from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth.google.oauth import oauth
from auth.config import GOOGLE_REDIRECT_URI
from users.schemas import UserAuthorizationCreate
from database import get_db
from starlette.requests import Request
from users.crud import get_user_by_email, create_user, create_user_registration
from users.types import Provider, AuthorizationStatus
from auth.tokens import create_access_token, create_refresh_token, hash_token
from users.services import add_user_authorization_token
from auth.schemas import TokenPayload
from auth.types import TokenScope

router = APIRouter(prefix="/auth/google", tags=["auth"])

@router.get("/login")
async def get_google_auth(request: Request):
    redirect_uri = GOOGLE_REDIRECT_URI or request.url_for('auth.google.callback')
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    return response

@router.get("/callback", name="auth.google.callback")
async def get_google_auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

    if not token:
        raise HTTPException(status_code=400, detail="Failed to obtain token from Google")
    
    user_info = token.get('userinfo')
    if not user_info:
        try:
            user_info = await oauth.google.userinfo(token=token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to obtain user info from Google: {str(e)}")
    
    user_email = user_info.get('email')
    user_name = user_info.get('name')
    user_picture = user_info.get('picture')

    user = get_user_by_email(db, email=user_email)
    if not user:
        user = create_user(db, user_name, user_email, user_picture)
        create_user_registration(db, user.user_id)
        redirect_url = "/onboarding"
    else:
        redirect_url = "/home"

    expires_at = token.get("expires_at")
    google_refresh_token = token.get("refresh_token")
    
    if google_refresh_token:
        hashed_refresh_token = hash_token(google_refresh_token)
        add_user_authorization_token(db, token=UserAuthorizationCreate(user_id=user.user_id, provider=Provider.GOOGLE, refresh_token=hashed_refresh_token, expires_at=expires_at, status=AuthorizationStatus.ACTIVE))

    access_token = create_access_token(TokenPayload(user_id=str(user.user_id), scope=TokenScope.ACCESS.value))
    refresh_token = create_refresh_token(TokenPayload(user_id=str(user.user_id), scope=TokenScope.REFRESH.value))

    redirect_response = RedirectResponse(url=redirect_url)
    redirect_response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax")
    redirect_response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="lax")

    return redirect_response
