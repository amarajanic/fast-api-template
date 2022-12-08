from datetime import timedelta
from auth.jwtgenerator import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, verify_tokon_password
from auth.schemas import ResetPassword, UserRegistrate
from role.model import DbRole
from user.model import DbUser
from user.schemas import UserLogin
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from auth.hash import bcrypt, verify
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="forgot-password")

async def validate_user_login(request: UserLogin, db: Session):
    user = db.query(DbUser).filter(DbUser.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid username or password")

    role = db.query(DbRole).filter(DbRole.id == user.role_id).first()
    
    
    if not verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "scope": role.name}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "scope": role.name}
    )
    return {"access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"}


async def registrate_user(request:UserRegistrate, db: Session):
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Your password and confirmation password do not match")
    
    dbUser = db.query(DbUser).filter(DbUser.email == request.email).first()

    if dbUser:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"User with that email already exists.")

    
    hashedPassword = bcrypt(request.password)
    new_user = DbUser(name=f"{request.first_name} {request.last_name}", email=request.email, password=hashedPassword, role_id=3)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def forgot_password(email: str, db: Session):
    dbUser = db.query(DbUser).filter(DbUser.email == email).first()
    if dbUser:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
        data={"sub": email, "pass": dbUser.password}, expires_delta=access_token_expires
        )
        reset_link = f"http://127.0.0.1:8000/reset-password"
        return {"email-token":token, "reset-link": reset_link}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with mail {email} doesn't exist.")

async def reset_password(request: ResetPassword ,db: Session, token: str = Depends(oauth2_scheme)):
    if request.password != request.confirm_password:
       raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Your password and confirmation password do not match")
    username = verify_tokon_password(token, db)
    
    dbUser = db.query(DbUser).filter(DbUser.email==username)

    hashedPassword = bcrypt(request.password)

    dbUser.update({
        DbUser.password: hashedPassword
    })
    db.commit()

    return {"deatil":"Password changed successfully"}

    


    