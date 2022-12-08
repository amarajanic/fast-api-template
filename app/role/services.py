from role.schemas import RoleDisplay
from sqlalchemy.orm import Session
from role.model import DbRole
from fastapi import HTTPException, status



async def get_roles(db: Session):
    roles = db.query(DbRole).all()
    return roles