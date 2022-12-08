from urllib import response
from fastapi import APIRouter, Depends, status, HTTPException, Security
from auth.jwtgenerator import create_new_access_token, verify_tokon_password
from auth.schemas import ResetPassword, UserRegistrate
from auth.services import forgot_password, registrate_user, reset_password, validate_user_login
from database.db import get_db
from user.schemas import UserDisplay, UserLogin
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer


router = APIRouter(tags=["authentication"])

security = HTTPBearer()


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    response = await validate_user_login(request, db)
    return response


@router.post("/registration", response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
async def create_new_user(request: UserRegistrate, db: Session = Depends(get_db)):
    response = await registrate_user(request,db)
    return response

@router.post("/forgot-password")
async def forgot_user_password(email:str, db: Session = Depends(get_db)):
    response = await forgot_password(email, db)
    return response

@router.post("/reset-password")
async def reset_user_password(request: ResetPassword, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    response = await reset_password(request, db, token)
    return response


@router.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),  db: Session = Depends(get_db)):
    refresh_token = credentials.credentials
    new_token = await create_new_access_token(refresh_token,db)
    return {'access_token': new_token}