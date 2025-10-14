from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urlencode
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from database import get_db
from models.user_model import User, Partnership
from .tokens import create_access_token, create_refresh_token
from schemas.token_schema import Token, TokenPayload
from schemas.user_schema import UserCreate, UserRead
from .config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_TOKEN_REQUEST_URI, GOOGLE_SCOPES

from fastapi import FastAPI, Request, Depends, Response 
from fastapi.middleware.cors import CORSMiddleware 
from authlib.integrations.starlette_client import OAuth 

# base_url add to a different file
# add the state to the scopes
# create a state generator function

# OAuth2 Setup

# oauth = OAuth()

# # OAuth library automatically handles state generation and validation
# oauth.register(
#     name='google',
#     client_id=GOOGLE_CLIENT_ID,
#     client_secret=GOOGLE_CLIENT_SECRET,
#     access_token_url=GOOGLE_TOKEN_REQUEST_URI,
#     authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
#     client_kwargs={
#         'scope': ' '.join(GOOGLE_SCOPES),
#         'access_type': 'offline',
#         'prompt': 'consent',
#     }
# )

# def create user  with basic information
# get user, based on email
# instead should i pass a pydantic model to create user?

# in terms of database what else do i need to create?
# i would need to store google tokens in database to be able to access them to send emails
# store my own refresh token in the cookie

# need to create a google user model to store google tokens, this would be tied to the user model by
# the user id? or what would it be tied to the user with?

async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(
        name=user.name,
        email=user.email,
        picture=user.picture,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


async def get_or_create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return UserRead.model_validate(existing_user)
    return create_user(user, db)

# hash the refresh token from google and store it in the database
# if this doesn't exist, need to go through google auth flow again to generate a new refresh token for google?
# so you need a google refresh token generator and your own token create function

# when refresh token expires, the frontend should redirect back to the login endpoint. this is handled by the frontend


    
# create and store session cookie?

# def get_google_auth_url():
#     base_url = "https://accounts.google.com/o/oauth2/v2/auth"
#     params = {
#         "client_id": GOOGLE_CLIENT_ID,
#         "redirect_uri": GOOGLE_REDIRECT_URI,
#         "response_type": "code",
#         "scope": " ".join(GOOGLE_SCOPES), # add a state variable
#         "access_type": "offline", # what does that mean?
#         "prompt": "consent", # what does that mean?
#     }
#     return f"{base_url}?{urlencode(params)}"

# async def get_google_auth_callback(code: str, db: Session = Depends(get_db)):
#     data = {
#         "code": code,
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "redirect_uri": GOOGLE_REDIRECT_URI,
#         "grant_type": "authorization_code"
#     }

#     async with httpx.AsyncClient() as client:
#         token_response = await client.post(GOOGLE_TOKEN_REQUEST_URI, data=data)
#         if token_response.status_code != 200:
#             raise HTTPException(status_code=400, detail="Invalid code")
#         tokens = token_response.json()

#     id_token_str = tokens.get("id_token")
#     user_info = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), GOOGLE_CLIENT_ID)

#     user = db.query(User).filter(User.email == user_info.get("email")).first()
#     if not user:
#         user = User(
#             name=user_info.get("name"),
#             email=user_info.get("email"),
#             picture=user_info.get("picture"),
#         )
#         db.add(user)
#         db.commit()


#     access_token = create_access_token(TokenPayload(sub=str(user.id)))
#     refresh_token = create_refresh_token(TokenPayload(sub=str(user.id)))

#     return Token(access_token=access_token, refresh_token=refresh_token)

# def generate_session():

# generate session
# generate state that is of the session
# store in session and the url
# return the url
# parse return token
# create new user -> return user
# get existing user -> return user
# access token + user id should be good for returning to frontend
# refresh token should be stored in a httponly cookie and then sent to the frontend
# frontend should store the access token in memory and use it for subsequent requests