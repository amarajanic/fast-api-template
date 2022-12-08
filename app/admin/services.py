from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from user.model import DbUser
from role.model import DbRole

async def update_permissions(user_id:int, role_id:int, db: Session):
    dbRole = db.query(DbRole).filter(DbRole.id == role_id).first()
    if dbRole is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} not found")

    dbUser = db.query(DbUser).filter(DbUser.id == user_id).update({
        DbUser.role_id: role_id
    })
    db.commit()
    if dbUser is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    
    return {"detail":f"User with id {user_id} updated to role {dbRole.name}."} 
