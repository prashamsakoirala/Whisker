from sqlalchemy.orm import Session
import uuid
from .models import Ownerships

# create ownership
def create_ownership(db: Session, partnership_id: uuid.UUID, cat_id: uuid.UUID) -> Ownerships:
	existing = db.query(Ownerships).filter(Ownerships.partnership_id == partnership_id, Ownerships.cat_id == cat_id).first()
	if existing:
		return existing
	ownership = Ownerships(partnership_id=partnership_id, cat_id=cat_id)
	db.add(ownership)
	db.commit()
	db.refresh(ownership)
	return ownership

# get ownership
# maybe one to one relationship 
def get_ownership_by_partnership_id(db: Session, partnership_id: uuid.UUID):
	return db.query(Ownerships).filter(Ownerships.partnership_id == partnership_id).first()

def get_ownership_by_cat_id(db: Session, cat_id: uuid.UUID):
	return db.query(Ownerships).filter(Ownerships.cat_id == cat_id).first()

# delete ownership
def delete_ownership(db: Session, partnership_id: uuid.UUID, cat_id: uuid.UUID) -> bool:
	ownership = db.query(Ownerships).filter(Ownerships.partnership_id == partnership_id, Ownerships.cat_id == cat_id).first()
	if not ownership:
		return False
	db.delete(ownership)
	db.commit()
	return True