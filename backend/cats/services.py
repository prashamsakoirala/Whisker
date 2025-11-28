# def decrement_happiness(cat_id: uuid.UUID, db: Session = Depends(get_db)):
#     try:
#         cat = db.get(Cat, cat_id)

#         if not cat:
#             raise print("Cat with id {cat_id} not found")

#         happiness_attribute = db.query(CatState).filter(CatState.cat_id == cat_id, CatState.state == CatStateEnum.HAPPINESS).first()

#         happiness_value = happiness_attribute.value

#         if happiness_value == 0:
#             raise print("Happiness attribute for cat with id {cat_id} at min value")
        
#         happiness_attribute.value = happiness_value - 1
#         happiness_attribute.last_updated = datetime.now(datetime.timezone.utc)

#         db.commit()
#         db.refresh(happiness_attribute)

#         return happiness_attribute

#     except Exception as e:
#         print("Error decrementing cat happiness: ", e)


# def decrement_hunger(cat_id: uuid.UUID, db: Session = Depends(get_db)):
#     try:
#         cat = db.get(CatState, cat_id)

#         if not cat:
#             raise print("Cat with id {cat_id} not found")

#         hunger_attribute = db.query(CatState).filter(CatState.cat_id == cat_id, CatState.state == CatStateEnum.HUNGER).first()

#         hunger_value = hunger_attribute.value

#         if hunger_value == 0:
#             raise print("Hunger attribute for cat with id {cat_id} at min value")
        
#         hunger_attribute.value = hunger_value - 1
#         hunger_attribute.last_updated = datetime.now(datetime.timezone.utc)

#         db.commit()
#         db.refresh(hunger_attribute)

#         return hunger_attribute

#     except Exception as e:
#         print("Error decrementing cat hunger: ", e)

# get_all_cats_by_partnership
# get_all_cats_by_user