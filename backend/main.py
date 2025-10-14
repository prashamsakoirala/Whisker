from fastapi import FastAPI
from api import user_routes, cat_routes
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from auth.config import SECRET_KEY as APP_SECRET_KEY
from auth.google import routes as auth_google_routes


app = FastAPI()

# Allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SessionMiddleware is required by Authlib's Starlette integration to access request.session
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_routes.router)
app.include_router(cat_routes.router)
app.include_router(auth_google_routes.router)

