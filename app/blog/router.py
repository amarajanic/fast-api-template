from typing import List, Optional
from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user

from blog.schemas import BlogDisplay, BlogInsert, BlogUpdate, OrderBy
from database.db import get_db
from blog.services import create_blog, delete_blog, get_blog_by_id, get_blogs, sync_blogs, update_blog
from user.schemas import RoleDisplay, UserLogin

router = APIRouter(prefix="/blogs", tags=["blogs"])

@router.get("/sync")
async def sync(db: Session = Depends(get_db)):
    response = await sync_blogs(db)
    return response

@router.post("", response_model=BlogDisplay, status_code=status.HTTP_201_CREATED)
async def create_new_blog(request: BlogInsert, db: Session = Depends(get_db)):
    response = await create_blog(request,db)
    return response


@router.get("", response_model=List[BlogDisplay])
async def get_all_blogs(search: Optional[str] = None, order_by: OrderBy = OrderBy.az, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: UserLogin = Security(get_current_user, scopes=["SuperAdmin"])):
    response = await get_blogs(db, search, order_by, skip, limit)
    return response

@router.get("/{id}", response_model=BlogDisplay)
async def get_blog(id:int, db: Session = Depends(get_db), current_user: UserLogin = Security(get_current_user, scopes=["SuperAdmin","User"])):
    response = await get_blog_by_id(id, db)
    return response

@router.delete("/{id}", response_model=BlogDisplay)
async def remove_blog(id:int, db: Session = Depends(get_db)):
    response = await delete_blog(id,db)
    return response

@router.put("/{id}")
async def put_blog(id:int,request: BlogUpdate, db: Session = Depends(get_db)):
    response = await update_blog(id, request,db)
    return response
    

