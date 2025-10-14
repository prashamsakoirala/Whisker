from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.cat_schema import *
from schemas.user_schema import *
from models.cat_model import *
from typing import Optional
from auth.dependencies import get_current_user, get_current_cat, get_current_partnership

router = APIRouter(prefix="/cats", tags=["cats"])

def create_cat_with_defaults(db: Session, name: str):
    cat = Cat(name = name)

    cat.state = [
        CatState(cat_id = cat.id, state = CatStateEnum.HUNGER, value = 3),
        CatState(cat_id = cat.id, state = CatStateEnum.HAPPINESS, value = 3)
    ]

    cat.inventory = [
        CatInventory(cat_id = cat.id, item = CatItemEnum.FISH, value = 5),
        CatInventory(cat_id = cat.id, item = CatItemEnum.TOY, value = 5)
    ]

    cat.animation = [
        CatAnimation(cat_id = cat.id, animation = CatAnimationEnum.IDLE)
    ]

    db.add(cat)
    db.commit()
    db.refresh(cat)

    return cat



# Done
@router.post("/", response_model=CatRead)
async def create_cat(cat_name: CatCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if not current_user.primary_partnership:
            raise HTTPException(status_code=400, detail="User does not have a primary partnership")

        if current_user.id != current_user.primary_partnership.primary_user_id:
            raise HTTPException(status_code=403, detail="Only the primary user can create the cat")

        new_cat = create_cat_with_defaults(db, cat_name.name)

        primary_partnership = current_user.primary_partnership 
        primary_partnership.cat_id = new_cat.id

        db.commit()
        db.refresh(new_cat)


        return CatRead(
            id = new_cat.id, 
            name = new_cat.name, 
            created_at = new_cat.created_at, 
            states = new_cat.state,
            inventory = new_cat.inventory,
            animation = new_cat.animation
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/active/", response_model=CatRead)
async def set_active_cat(cat_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        cat = db.get(Cat, cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        
        if current_user.primary_partnership.cat_id != cat_id:
            raise HTTPException(status_code=403, detail="Unidentified cat")
        
        current_user.active_cat_association = cat

        return CatRead(
            id = cat.id, 
            name = cat.name, 
            created_at = cat.created_at, 
            states = cat.state,
            inventory = cat.inventory,
            animation = cat.animation            
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active/", response_model=CatRead)
async def get_active_cat(cat: Cat = Depends(get_current_cat)):
    try:
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        return cat
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/active/inventory/", response_model=CatInventoryRead | list[CatInventoryRead])
async def get_active_cat_inventory(cat: Cat = Depends(get_current_cat), item_name: Optional[CatItemEnum] = None, db: Session = Depends(get_db)):
    try:

        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")

        query = db.query(CatInventory).filter(CatInventory.cat_id == cat.id)

        if item_name:
            item = query.filter(CatInventory.item == item_name).first()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item  

        items = query.all()
        return items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/active/state/", response_model=CatStateRead | list[CatStateRead])
async def get_cat_state(cat: Cat = Depends(get_current_cat), state_type: Optional[CatStateEnum] = None, db: Session = Depends(get_db)):
    try:
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")

        query = db.query(CatState).filter(CatState.cat_id == cat.id)
        if state_type:
            state = query.filter(CatState.state == state_type).first()
            if not state:
                raise HTTPException(status_code=404, detail="State not found")
            return state
        
        states = query.all()
        return states
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/active/animation/", response_model=CatAnimationRead)
async def get_cat_animation(cat: Cat = Depends(get_current_cat), db: Session = Depends(get_db)):
    try:

        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")

        animation = db.query(CatAnimation).filter(CatAnimation.cat_id == cat.id).first()
        
        if not animation:
            raise HTTPException(status_code=404, detail="Animation not found")
        
        return animation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/active/hunger/", response_model=CatStateRead)
async def update_cat_hunger(cat: Cat = Depends(get_current_cat), db: Session = Depends(get_db)):
    try:
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        
        hunger_attribute = db.query(CatState).filter(CatState.cat_id == cat.id, CatState.state == CatStateEnum.HUNGER).first()

        hunger_value = hunger_attribute.value

        if hunger_value == 3:
            raise HTTPException(status_code=409, detail="Hunger attribute at max value")
                    
        hunger_attribute.value = hunger_value + 1
        hunger_attribute.last_updated = datetime.now(datetime.timezone.utc)

        db.commit()
        db.refresh(hunger_attribute)

        return hunger_attribute
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/active/happiness/", response_model=CatStateRead)
async def update_cat_happiness(cat: Cat = Depends(get_current_cat), db: Session = Depends(get_db)):
    try:

        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        
        happiness_attribute = db.query(CatState).filter(CatState.cat_id == cat.id, CatState.state == CatStateEnum.HAPPINESS).first()

        happiness_value = happiness_attribute.value

        if happiness_value == 3:
            raise HTTPException(status_code=409, detail="Happiness attribute at max value")
                    
        happiness_attribute.value = happiness_value + 1
        happiness_attribute.last_updated = datetime.now(datetime.timezone.utc)

        db.commit()
        db.refresh(happiness_attribute)

        return happiness_attribute
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def decrement_happiness(cat_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        cat = db.get(Cat, cat_id)

        if not cat:
            raise print("Cat with id {cat_id} not found")

        happiness_attribute = db.query(CatState).filter(CatState.cat_id == cat_id, CatState.state == CatStateEnum.HAPPINESS).first()

        happiness_value = happiness_attribute.value

        if happiness_value == 0:
            raise print("Happiness attribute for cat with id {cat_id} at min value")
        
        happiness_attribute.value = happiness_value - 1
        happiness_attribute.last_updated = datetime.now(datetime.timezone.utc)

        db.commit()
        db.refresh(happiness_attribute)

        return happiness_attribute

    except Exception as e:
        print("Error decrementing cat happiness: ", e)


def decrement_hunger(cat_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        cat = db.get(CatState, cat_id)

        if not cat:
            raise print("Cat with id {cat_id} not found")

        hunger_attribute = db.query(CatState).filter(CatState.cat_id == cat_id, CatState.state == CatStateEnum.HUNGER).first()

        hunger_value = hunger_attribute.value

        if hunger_value == 0:
            raise print("Hunger attribute for cat with id {cat_id} at min value")
        
        hunger_attribute.value = hunger_value - 1
        hunger_attribute.last_updated = datetime.now(datetime.timezone.utc)

        db.commit()
        db.refresh(hunger_attribute)

        return hunger_attribute

    except Exception as e:
        print("Error decrementing cat hunger: ", e)


# ### Websockets

# # Broadcast cat hunger

# # Broadcast cat happiness

# # Broadcast cat animation


# ### Other Functions

# # Setting new animation
# def set_animation():

#     return

