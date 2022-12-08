from typing import List, Optional
from pydantic import BaseModel

class BlogDisplay(BaseModel):
    id:int
    title: str
    body: str
    class Config:
         orm_mode = True

class RoleDisplay(BaseModel):
    name: str
    class Config:
        orm_mode = True

class UserDisplay(BaseModel):
    id: int
    name:str
    email:str
    blogs: List[BlogDisplay]
    role: RoleDisplay
    class Config:
         orm_mode = True


class UserInsert(BaseModel):
    name:str
    email:str
    password:str
    role_id: int
    class Config:
         orm_mode = True

class UserUpdate(UserInsert):
    class Config:
         orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str

