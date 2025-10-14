from datetime import datetime, timedelta, timezone
import jwt
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from schemas.token_schema import TokenPayload

def create_access_token(data: TokenPayload, expires_time: timedelta | None = None):
    to_encode = data.model_dump() # Copying data

    # While expires time is not None

    if expires_time:
        expire = datetime.now(timezone.utc) + expires_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Update expire parameter of data
    to_encode.update({"exp" : expire, "scope": "access_token"})

    # Return encoded data
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
# No need for an expire time since refresh is longer term
def create_refresh_token(data: TokenPayload):
    to_encode = data.model_dump() # Copying data

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # Update expire parameter of data
    to_encode.update({"exp" : expire, "scope" : "refresh_token"})

    # Return encoded data
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload.model_validate(payload)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None