from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import uuid
from .models import Partnerships
from ownerships.models import Ownerships


def create_partnership(db: Session, partner_1_id: uuid.UUID, partner_2_id: uuid.UUID) -> Partnerships:
	partnership = Partnerships(partner_1_id=partner_1_id, partner_2_id=partner_2_id)
	db.add(partnership)
	db.commit()
	db.refresh(partnership)
	return partnership


def get_partnership_by_user_id(db: Session, user_id: uuid.UUID) -> Optional[Partnerships]:
	return db.query(Partnerships).filter(
		or_(Partnerships.partner_1_id == user_id, Partnerships.partner_2_id == user_id)
	).first()


def get_partnership_by_partnership_id(db: Session, partnership_id: uuid.UUID) -> Optional[Partnerships]:
	return db.query(Partnerships).filter(Partnerships.partnership_id == partnership_id).first()


def get_all_partnerships(db: Session) -> List[Partnerships]:
	return db.query(Partnerships).all()


def delete_partnership(db: Session, partnership_id: uuid.UUID) -> bool:
	partnership = get_partnership_by_partnership_id(db, partnership_id)
	if not partnership:
		return False
	db.delete(partnership)
	db.commit()
	return True


def get_all_partnerships_for_user(db: Session, user_id: uuid.UUID) -> List[Partnerships]:
	return db.query(Partnerships).filter(
		or_(Partnerships.partner_1_id == user_id, Partnerships.partner_2_id == user_id)
	).all()