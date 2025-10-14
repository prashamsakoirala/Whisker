from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.google.oauth import oauth
from database import get_db
from starlette.requests import Request

router = APIRouter(prefix="/auth/google", tags=["auth"])

@router.get("/login") #added start, should be fine
async def get_google_auth(request: Request):
    redirect_uri = request.url_for('auth.google.callback')
    # await and return the response
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    return response

@router.get("/callback", name="auth.google.callback")
async def get_google_auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    
    user_info = token.get('userinfo')
    if not user_info: # if userinfo not in token, fetch it
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo', token=token)
        user_info = resp.json()
    
    # create new user with user_info it it does not exist in DB


    
    request.session['user'] = {
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'picture': user_info.get('picture'),
    }
    request.session['token'] = token
    
    return token

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
        