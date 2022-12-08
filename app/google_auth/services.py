from datetime import timedelta
from sqlalchemy.orm import Session
from auth.jwtgenerator import create_access_token, create_refresh_token
from role.model import DbRole
from user.model import DbUser
from fastapi import HTTPException, status

async def validate_user(db: Session, email:str):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    if user:
        return user
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User with provided email doesn't exist.")

async def generate_tokens(user, db: Session):
    role = db.query(DbRole).filter(DbRole.id == user.role_id).first()
    access_token = create_access_token(
        data={"sub": user.email, "scope": role.name}, expires_delta=timedelta(minutes=2)
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "scope": role.name}
    )
    return {"access-token": access_token, "refresh_token": refresh_token}