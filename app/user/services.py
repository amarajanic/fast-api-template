from sqlalchemy.orm import Session
from blog.model import DbBlog
from fastapi import HTTPException, status
from user.model import DbUser

from user.schemas import UserInsert, UserUpdate

from auth.hash import bcrypt

async def create_user(request:UserInsert, db: Session):
    hashedPassword = bcrypt(request.password)
    new_user = DbUser(name=request.name, email=request.email, password=hashedPassword, role_id=request.role_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def get_users(db: Session):
    users = db.query(DbUser).all()
    return users

async def get_user_by_id(id:int, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if user is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

async def delete_user(id:int, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if user is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return user

async def update_user(id:int, request: UserUpdate, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id).update({
        DbUser.name: request.name,
        DbUser.email: request.email,
        DbUser.password: request.password,
        DbUser.role_id: request.role_id
    })
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    db.commit()
    return {"detail":f"User with id {id} updated."} 
    