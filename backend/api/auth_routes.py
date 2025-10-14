from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth.dependencies import refresh_access_token
from database import get_db

# router = APIRouter(prefix="/auth", tags=["auth"])

# @router.get("/google/start") #added start, should be fine
# async def get_google_auth():
#     auth_url = get_google_auth_url()
#     return RedirectResponse(url=auth_url)

# @router.get("/google/callback")
# async def google_callback(code: str, db: Session = Depends(get_db)):
#     token = await get_google_auth_callback(code, db)
#     return token

# @router.post("/refresh")
# async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
#     return await refresh_access_token(refresh_token, db)