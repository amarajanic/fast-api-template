from role.schemas import RoleDisplay
from sqlalchemy.orm import Session
from role.model import DbRole
from fastapi import HTTPException, status


async def get_roles(db: Session):
    roles = db.query(DbRole).all()
    return roles


async def sync_data(db: Session):
    user = DbRole(name="User")
    db.add(user)
    admin = DbRole(name="Admin")
    db.add(admin)
    superadmin = DbRole(name="SuperAdmin")
    db.add(superadmin)
    db.commit()
    db.refresh(user)
    db.refresh(admin)
    db.refresh(superadmin)
    return "Ok"
