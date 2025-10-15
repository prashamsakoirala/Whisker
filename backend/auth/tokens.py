from datetime import datetime, timedelta, timezone
import jwt
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from .schemas import TokenPayload
from .types import TokenScope
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(data: TokenPayload, scope: TokenScope, expires_time: timedelta | None = None):
    to_encode = data.model_dump() # Copying data
    expire = datetime.now(timezone.utc) + expires_time
    to_encode.update({"exp" : expire, "scope": scope.value})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# what if i want the expire time to be constant??? lol i dont need to pass it in?
def create_access_token(data: TokenPayload, expires_time: timedelta | None = None):
    if expires_time is None:
        expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, TokenScope.ACCESS, expires_time)
    
# No need for an expire time since refresh is longer term
def create_refresh_token(data: TokenPayload, expires_time: timedelta | None = None):
    if expires_time is None:
        expires_time = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(data, TokenScope.REFRESH, expires_time)

# all this knows is given a token, decode it; doesnt need to pass in cookie thats another layer
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload.model_validate(payload)
    except jwt.ExpiredSignatureError:
        return ValueError("Token has expired")
    except jwt.PyJWTError:
        return ValueError("Invalid token")
    
def hash_token(token: str) -> str:
    return pwd_context.hash(token)

def verify_token(plain_token: str, hashed_token: str) -> bool:
    return pwd_context.verify(plain_token, hashed_token)