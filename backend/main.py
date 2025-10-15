from fastapi import FastAPI
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from auth.config import SECRET_KEY as APP_SECRET_KEY
from auth.google import routes as auth_google_routes
from users import routes as user_routes


app = FastAPI()

# SessionMiddleware is required by Authlib's Starlette integration to access request.session
# Set https_only=False for local development (use True in production with HTTPS)
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY, https_only=False)

# Create DB tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_google_routes.router)
app.include_router(user_routes.router)


