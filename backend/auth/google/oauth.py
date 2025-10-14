from auth.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_TOKEN_REQUEST_URI, GOOGLE_SCOPES
from authlib.integrations.starlette_client import OAuth 

# OAuth2 Setup
oauth = OAuth()

# OAuth library automatically handles state generation and validation
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url=GOOGLE_TOKEN_REQUEST_URI,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    client_kwargs={
        'scope': ' '.join(GOOGLE_SCOPES),
        'access_type': 'offline',
        'prompt': 'consent',
    }
)