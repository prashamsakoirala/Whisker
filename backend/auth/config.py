import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Google OAuth Config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_TOKEN_REQUEST_URI = "https://oauth2.googleapis.com/token"
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile", 
    "https://www.googleapis.com/auth/userinfo.email",
]
