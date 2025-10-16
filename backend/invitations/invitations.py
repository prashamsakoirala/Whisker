import jwt
from .config import SECRET_KEY, SALT, INVITATION_TOKEN_EXPIRE_MINUTES, ALGORITHM
from .schemas import InvitationTokenPayload, InvitationTokenDecoded
from datetime import timedelta, datetime, timezone

def create_invitation_token(data: InvitationTokenPayload):
    to_encode = data.model_dump() # Copying data
    expire = datetime.now(timezone.utc) + timedelta(minutes=INVITATION_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, SECRET_KEY + SALT, algorithm=ALGORITHM)

def decode_invitation_token(token: str) -> InvitationTokenDecoded:
    try:
        payload = jwt.decode(token, SECRET_KEY + SALT, algorithms=[ALGORITHM])
        # Extract exp and convert to expires_at
        expires_at = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
        return InvitationTokenDecoded(
            invitee_email=payload['invitee_email'],
            inviter_email=payload['inviter_email'],
            expires_at=expires_at
        )
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.PyJWTError:
        raise ValueError("Invalid token")

# dont know what to do for hte above so i create it and then the user sends the toke
# then once the user tsends the token then another user grabs that token encoded into the button
# then they click onto it and it decodes it and grabs the email and user ID
# that is associated with that token when decoding make sure that the user
# who is accepting the invitation is not the same user who sent it OR make a check to make sure
# invitation cannot be the same user that is sendin git
# when accepting make sure the current user email id is equal to the email id in the token
# if not then throw unauthorized error

# hash invitation code
# make sure user cannot send invitation to same user twice if they already are linked together in a partnership
# allow user to revoke invitation if its pending by pressing back button