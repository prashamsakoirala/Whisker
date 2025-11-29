from sqlalchemy.orm import Session
import uuid
from typing import Optional, List
from .types import *
from .models import *

# get cat
def get_cat(db: Session, cat_id: uuid.UUID) -> Optional[Cat]:
    return db.query(Cat).filter(Cat.id == cat_id).first()

def get_cat_animation(db: Session, cat_id: uuid.UUID) -> Optional[CatAnimation]:
    return db.query(CatAnimation).filter(CatAnimation.cat_id == cat_id).first()

def get_cat_states(db: Session, cat_id: uuid.UUID) -> List[CatState]:
    return db.query(CatState).filter(CatState.cat_id == cat_id).all()

def get_cat_inventory(db: Session, cat_id: uuid.UUID) -> List[CatState]:
    return db.query(CatInventory).filter(CatInventory.cat_id == cat_id).all()

def get_cat_state_by_type(db: Session, cat_id: uuid.UUID, state_type: CatStateEnum) -> Optional[CatState]:
    return db.query(CatState).filter(CatState.cat_id == cat_id, CatState.state == state_type).first()

def get_cat_inventory_by_type(db: Session, cat_id: uuid.UUID, item_type: CatItemEnum) -> Optional[CatInventory]:
    return db.query(CatInventory).filter(CatInventory.cat_id == cat_id, CatInventory.item == item_type).first()

# update cat
def update_cat_state(db: Session, cat_id: uuid.UUID, state: CatStateEnum, value: int) -> CatState:
    cat = get_cat_state_by_type(db, cat_id, state)
    if not cat:
        return None
    if value is not None:
        cat.value = value
    db.commit()
    db.refresh(cat)
    return cat

def update_cat_inventory(db: Session, cat_id: uuid.UUID, item: CatItemEnum, value: int) -> CatInventory:
    cat = get_cat_inventory_by_type(db, cat_id, item)
    if not cat:
        return None
    if value is not None:
        cat.value = value
    db.commit()
    db.refresh(cat)
    return cat

def update_cat_animation(db: Session, cat_id: uuid.UUID, animation: CatAnimationEnum) -> CatState:
    cat = get_cat_animation(db, cat_id)
    if not cat:
        return None
    if animation is not None:
        cat.animation = animation
    db.commit()
    db.refresh(cat)
    return cat

# create cat, need to create a cat based on the current user's partnership? need to find a way to link this together
def create_cat(db: Session, partnership_id: uuid.UUID) -> Cat:
    # finish storing cat info
    cat = Cat()
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

# delete cat
def delete_cat(db: Session, cat_id: uuid.UUID) -> bool:
    cat = get_cat(db, cat_id)
    if not cat:
        return False
    db.delete(cat)
    db.commit()
    return True