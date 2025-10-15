from sqlalchemy.orm import Session
from users.crud import *
from users.schemas import *
# business logic layer, calls external apis, etc

# register new user, make sure registration status is created along with authorization token...

def register_user(db: Session, user: UserCreate) -> UserResponse:
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    user = create_user(db, user.name, user.email, user.profile_picture)
    create_user_registration(db, user.id)

    return UserResponse(from_orm=user)

# add user authorization token
# just add an entry without removing/editing existing ones
# incorrect get user authorization
# TODO FIX
def add_user_authorization_token(db: Session, token: UserAuthorizationCreate) -> UserAuthorization:
    existing = get_user_authorization(db, token.user_id, token.provider, token.status == AuthorizationStatus.ACTIVE)
    if existing:
        raise ValueError(f"There exists a valid active {token.provider} authorization token for this user")
    auth = UserAuthorization(**token.model_dump())
    db.add(auth)
    db.commit()
    db.refresh(auth)
    return UserAuthorizationResponse(from_orm=auth)

# register spotify

# update user registration status
def update_registration_status(db: Session, status: UserRegistrationUpdate) -> UserRegistrationResponse:
    current_status = get_user_registration(db, status.user_id)
    if not current_status:
        raise ValueError("User registration status not found")
    if current_status.status == status.status:
        return UserRegistrationResponse(from_orm=current_status)
    
    reg = update_user_registration(db, status.user_id, status.status)
    return UserRegistrationResponse(from_orm=reg)

# get user registration status
def get_registration_status(db: Session, user_id: uuid.UUID) -> UserRegistrationResponse:
    reg = get_user_registration(db, user_id)
    if not reg:
        raise ValueError("User registration status not found")
    return UserRegistrationResponse(from_orm=reg)

def update_user_refresh_token_status(db: Session, token: UserAuthorizationCreate) -> UserAuthorizationResponse:
    # find the active authorization for this user/provider before updating
    existing = get_user_authorization(db, token.user_id, token.provider, AuthorizationStatus.ACTIVE)
    if not existing:
        raise ValueError(f"No active {token.provider} authorization token found for this user")
    auth = update_user_authorization(db, token.user_id, token.provider, token.refresh_token, token.expires_at, token.status)
    return UserAuthorizationResponse(from_orm=auth)

# get user refresh token, defaults to active token if not input
def get_user_refresh_token(db: Session, user_id: uuid.UUID, token_provider: str, token_status: AuthorizationStatus = AuthorizationStatus.ACTIVE) -> UserAuthorizationResponse:
    existing = get_user_authorization(db, user_id, token_provider, token_status)
    if not existing:
        raise ValueError(f"No {token_status} {token_provider} authorization token found for this user")
    return UserAuthorizationResponse(from_orm=existing)

# TODO DO THIS ONCE YOU HAVE CRUD FOR SPOTIFY
# get user music personality

# update user music personality

# TODO DO THIS ONCE YOU HAVE CREATED CRUD FOR CATS AND PARTNERSHIPS
# get user all cats

# get user all partnerships

# get user specific partnership

# get user specific cat

# get user partnership associated with a specific cat

