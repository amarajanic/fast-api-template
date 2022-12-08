from typing import List
from pydantic import BaseModel

class UserDisplay(BaseModel):
    name:str
    email:str
    class Config:
         orm_mode = True

class RoleDisplay(BaseModel):
    name: str
    users: List[UserDisplay]
    class Config:
        orm_mode = True
