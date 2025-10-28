from sqlalchemy.orm import Session
from users.crud import *
from users.schemas import *


def register_user(db: Session, user: UserCreate) -> UserResponse:
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    user = create_user(db, user.name, user.email, user.profile_picture)
    create_user_registration(db, user.user_id)

    return UserResponse.model_validate(user)


def add_user_authorization_token(db: Session, token: UserAuthorizationCreate) -> UserAuthorization:
    existing = get_user_authorization(db, token.user_id, token.provider, token.status == AuthorizationStatus.ACTIVE)
    if existing:
        raise ValueError(f"There exists a valid active {token.provider} authorization token for this user")
    auth = UserAuthorization(**token.model_dump())
    db.add(auth)
    db.commit()
    db.refresh(auth)
    return UserAuthorizationResponse.model_validate(auth)


def update_registration_status(db: Session, status: UserRegistrationUpdate) -> UserRegistrationResponse:
    current_status = get_user_registration(db, status.user_id)
    if not current_status:
        raise ValueError("User registration status not found")
    if current_status.status == status.status:
        return UserRegistrationResponse.model_validate(current_status)
    
    reg = update_user_registration(db, status.user_id, status.status)
    return UserRegistrationResponse.model_validate(reg)


def get_registration_status(db: Session, user_id: uuid.UUID) -> UserRegistrationResponse:
    reg = get_user_registration(db, user_id)
    if not reg:
        raise ValueError("User registration status not found")
    return UserRegistrationResponse.model_validate(reg)


def update_user_refresh_token_status(db: Session, token: UserAuthorizationCreate) -> UserAuthorizationResponse:
    existing = get_user_authorization(db, token.user_id, token.provider, AuthorizationStatus.ACTIVE)
    if not existing:
        raise ValueError(f"No active {token.provider} authorization token found for this user")
    auth = update_user_authorization(db, token.user_id, token.provider, token.refresh_token, token.expires_at, token.status)
    return UserAuthorizationResponse.model_validate(auth)

# gets the corresponding active token
def get_user_refresh_token(db: Session, user_id: uuid.UUID, token_provider: str, token_status: AuthorizationStatus = AuthorizationStatus.ACTIVE) -> UserAuthorizationResponse:
    existing = get_user_authorization(db, user_id, token_provider, token_status)
    if not existing:
        raise ValueError(f"No {token_status} {token_provider} authorization token found for this user")
    return UserAuthorizationResponse.model_validate(existing)

# how to return a list of them
def get_user_all_active_refresh_token(db: Session, user_id: uuid.UUID) -> UserAuthorizationResponse:
    existing = get_user_authorization(db, user_id, AuthorizationStatus.ACTIVE)
    if not existing:
        raise ValueError(f"No active authorization tokens found for this user")
    # TODO FIX THIS, return the list of models
    return
    # return UserAuthorizationResponse.model_validate(existing)

# TODO DO THIS ONCE YOU HAVE CRUD FOR SPOTIFY
# get user music personality
# register spotify
# update user music personality

# TODO DO THIS ONCE YOU HAVE CREATED CRUD FOR CATS AND PARTNERSHIPS
# get user all cats

# get user all partnerships

# get user specific partnership

# get user specific cat

# get user partnership associated with a specific cat

