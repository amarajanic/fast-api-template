from typing import List
from role.services import sync_data
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from role.schemas import RoleDisplay

from database.db import get_db
from role.services import get_roles

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/sync")
async def sync_roles(db: Session = Depends(get_db)):
    response = await sync_data(db)
    return response


@router.get("", response_model=List[RoleDisplay])
async def get_all_roles(db: Session = Depends(get_db)):
    response = await get_roles(db)
    return response
