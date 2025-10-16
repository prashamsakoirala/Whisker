import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
SALT = os.getenv("SALT")
INVITATION_TOKEN_EXPIRE_MINUTES = 5