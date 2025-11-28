# create partnership
# services
from sqlalchemy.orm import Session

from .models import Partnerships
from .crud import create_partnership, get_partnership_by_user_id, get_partnership_by_partnership_id, get_all_partnerships_for_user
import uuid
from users.crud import get_user
# create new partnership
    # need to validate that both users exist
    # prevent self partnership
    # check for existing partnership
    # then create partnership

def create_new_partnership(db: Session, partner_1_id: uuid.UUID, partner_2_id: uuid.UUID) -> Partnerships:
    # validate both users exist
    user1 = get_user(db, partner_1_id)
    user2 = get_user(db, partner_2_id)
    if not user1 or not user2:
        raise ValueError("One or both users do not exist")
    # prevent self partnership
    if partner_1_id == partner_2_id:
        raise ValueError("Cannot create partnership with oneself")
    # check for existing partnership
    partners = get_all_partnerships_for_user(db, partner_1_id)
    for entry in partners:
        if entry.partner_1_id == partner_2_id or entry.partner_2_id == partner_2_id:
            raise ValueError("Partnership exists for users")
    # create partnership
    return create_partnership(db, partner_1_id, partner_2_id)

