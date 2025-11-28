from sqlalchemy.orm import Session
import uuid
from .types import *
from .models import *

# get cat
def get_cat(db: Session, cat_id: uuid.UUID):
    return db.query(Cat).filter(Cat.id == cat_id).first()

def get_cat_animation(db: Session, cat_id: uuid.UUID):
    return db.query(CatAnimation).filter(CatAnimation.cat_id == cat_id).first()

def get_cat_states(db: Session, cat_id: uuid.UUID):
    return db.query(CatState).filter(CatState.cat_id == cat_id).all()

def get_cat_inventory(db: Session, cat_id: uuid.UUID):
    return db.query(CatInventory).filter(CatInventory.cat_id == cat_id).all()

def get_cat_state_by_type(db: Session, cat_id: uuid.UUID, state_type: CatStateEnum):
    return db.query(CatState).filter(CatState.cat_id == cat_id, CatState.state == state_type).first()

def get_cat_inventory_by_type(db: Session, cat_id: uuid.UUID, item_type: CatItemEnum):
    return db.query(CatInventory).filter(CatInventory.cat_id == cat_id, CatInventory.item == item_type).first()

# update cat
def update_cat_state(db: Session, cat_id: uuid.UUID, state: CatStateEnum, value: int):
    return 
def update_cat_inventory(db: Session, cat_id: uuid.UUID, state: CatItemEnum, value: int):
    return
def update_cat_animation(db: Session, cat_id: uuid.UUID, state: CatAnimationEnum):
    return

# create cat, need to create a cat based on the current user's partnership?
def create_cat(db: Session):
    return
# delete cat
def delete_cat(db: Session, cat_id: uuid.UUID):
    return 