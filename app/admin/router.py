from fastapi import APIRouter, Depends, status, HTTPException, Security
from sqlalchemy.orm import Session
from admin.services import update_permissions
from auth.oauth2 import get_current_user
from database.db import get_db
from user.schemas import UserLogin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.put("/user/permissions/", status_code=status.HTTP_200_OK)
async def update_user_permissions(user_id:int, role_id:int, db: Session = Depends(get_db), current_user: UserLogin = Security(get_current_user, scopes=["SuperAdmin"])):
    response = await update_permissions(user_id,role_id, db)
    return response