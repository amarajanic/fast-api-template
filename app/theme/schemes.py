from typing import List
from pydantic import BaseModel

class ThemeDisplay(BaseModel):
    id:int
    name: str
    class Config:
        orm_mode = True

class ThemeInsert(BaseModel):
    name: str
    class Config:
        orm_mode = True