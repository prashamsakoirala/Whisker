from auth.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_TOKEN_REQUEST_URI, GOOGLE_SCOPES
from authlib.integrations.starlette_client import OAuth 

# OAuth2 Setup
oauth = OAuth()

# OAuth library automatically handles state generation and validation
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent',
    }
)