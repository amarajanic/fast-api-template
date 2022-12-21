from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from user.schemas import UserDisplay, UserInsert, UserUpdate

from database.db import get_db
from user.services import create_user, delete_user, get_user_by_id, get_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
async def create_new_user(request: UserInsert, db: Session = Depends(get_db)):
    response = await create_user(request, db)
    return response


@router.get("", response_model=List[UserDisplay])
async def get_all_users(db: Session = Depends(get_db)):
    response = await get_users(db)
    return response


@router.get("/{id}", response_model=UserDisplay)
async def get_user(id: int, db: Session = Depends(get_db)):
    response = await get_user_by_id(id, db)
    return response


@router.delete("/{id}", response_model=UserDisplay)
async def remove_user(id: int, db: Session = Depends(get_db)):
    response = await delete_user(id, db)
    return response


@router.put("/{id}")
async def put_user(id: int, request: UserUpdate, db: Session = Depends(get_db)):
    response = await update_user(id, request, db)
    return response
