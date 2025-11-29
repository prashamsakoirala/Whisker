''' this should be admin '''
# POST /partnerships/
# GET /partnerships/{id}

# GET /me/partnerships/
# GET /me/partnerships/{partnership_id}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Partnerships
from .schemas import PartnershipResponse
from .dependencies import get_current_user_partnerships
from typing import List
import uuid

router = APIRouter(prefix="/partnerships", tags=["partnerships"])

@router.get("/me", response_model=List[PartnershipResponse])
async def read_current_user_partnerships(current_user_partnerships: List[Partnerships] = Depends(get_current_user_partnerships)):
    try:
        return [PartnershipResponse.model_validate(p) for p in current_user_partnerships]
    except ValueError as e:
        raise 

@router.get("/me/{partnership_id}", response_model=PartnershipResponse)
async def read_current_user_partnership(partnership_id: uuid.UUID, current_user_partnerships: List[Partnerships] = Depends(get_current_user_partnerships)):
    for p in current_user_partnerships:
        if p.partnership_id == partnership_id:
            return PartnershipResponse.model_validate(p)

    raise HTTPException(status_code=404, detail="Partnership not found")