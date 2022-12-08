from typing import Optional,List
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class UserRegistrate(BaseModel):
    first_name: str
    last_name: str
    email: str #as username
    password: str
    confirm_password: str

class ResetPassword(BaseModel):
    password: str
    confirm_password: str