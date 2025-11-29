# create partnership
# services
from sqlalchemy.orm import Session
from .models import Partnerships
from .crud import create_partnership, get_all_partnerships_for_user
import uuid
from users.crud import get_user

def create_new_partnership(db: Session, partner_1_id: uuid.UUID, partner_2_id: uuid.UUID) -> Partnerships:

    user1 = get_user(db, partner_1_id)
    user2 = get_user(db, partner_2_id)
    if not user1 or not user2:
        raise ValueError("One or both users do not exist")

    if partner_1_id == partner_2_id:
        raise ValueError("Cannot create partnership with oneself")

    partners = get_all_partnerships_for_user(db, partner_1_id)
    for entry in partners:
        if entry.partner_1_id == partner_2_id or entry.partner_2_id == partner_2_id:
            raise ValueError("Partnership exists for users")

    return create_partnership(db, partner_1_id, partner_2_id)

