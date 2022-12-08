from pydantic import BaseModel
from theme.schemes import ThemeDisplay

from user.schemas import RoleDisplay

from enum import Enum

class OrderBy(Enum):
    az = "az"
    za = "za"

class UserDisplay(BaseModel):
    id: int
    name:str
    email:str
    role: RoleDisplay
    class Config:
         orm_mode = True

class BlogDisplay(BaseModel):
    id:int
    title: str
    body: str
    user: UserDisplay
    theme: ThemeDisplay
    class Config:
         orm_mode = True

class BlogInsert(BaseModel):
    title: str
    body:str
    user_id: int
    theme_id: int
    class Config:
         orm_mode = True

class BlogUpdate(BlogInsert):
    theme_id: int
    class Config:
         orm_mode = True