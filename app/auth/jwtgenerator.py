from datetime import timedelta
from datetime import datetime
from typing import Any, Union
from jose import jwt, JWTError
from auth.schemas import TokenData
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import SecurityScopes
from pydantic import ValidationError

from user.model import DbUser


SECRET_KEY = "19d27e093faa6ca1556c174164b7a9593b93f6099f6f0f4bda6cf63b89e8d3b7" #for refresh and access
ALGORITHM = "HS256"                                                             #should be in .env file
ACCESS_TOKEN_EXPIRE_MINUTES = 2 #is for testing purposes, should be 60 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 #is for testing purposes, should be 7 days


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": data.get("sub"), "scope": data.get("scope")}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_token(security_scopes: SecurityScopes, token:str, credentials_exception):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    
    user_scopes = []

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        scope: str = payload.get("scope")
        if scope is None:
            raise credentials_exception
        token_scopes = payload.get("scope", [])
    except (JWTError, ValidationError):
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope in token_scopes:
            user_scopes.append(scope)
    if not user_scopes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

def verify_tokon_password(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        password: str = payload.get("pass")
        username: str = payload.get("sub")
        dbUser = db.query(DbUser).filter(DbUser.email == username).first()

        if password != dbUser.password:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access token already used",
        headers={"WWW-Authenticate": "Bearer"},
        )
        if username is None:
            raise credentials_exception
        return username   
    except (JWTError, ValidationError):
        raise credentials_exception


async def create_new_access_token(refresh_token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        dbUser = db.query(DbUser).filter(DbUser.email == username).first()
        if dbUser is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "User doesn't exist")
        access_token = create_access_token(
        data=payload
        )
        return access_token
    except JWTError:
        raise credentials_exception
