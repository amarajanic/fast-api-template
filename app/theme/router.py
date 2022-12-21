from typing import List
from app.theme.services import sync_data
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from theme.schemes import ThemeDisplay, ThemeInsert

from database.db import get_db
from theme.services import get_themes, create_theme

router = APIRouter(prefix="/themes", tags=["themes"])


@router.get("/sync")
async def sync_roles(db: Session = Depends(get_db)):
    response = await sync_data(db)
    return response


@router.get("", response_model=List[ThemeDisplay])
async def get_all_themes(db: Session = Depends(get_db)):
    response = await get_themes(db)
    return response


@router.post("", response_model=ThemeDisplay, status_code=status.HTTP_201_CREATED)
async def create_new_theme(request: ThemeInsert, db: Session = Depends(get_db)):
    response = await create_theme(request, db)
    return response
