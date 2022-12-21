from role.schemas import RoleDisplay
from sqlalchemy.orm import Session
from theme.model import DbTheme
from fastapi import HTTPException, status

from theme.schemes import ThemeInsert


async def sync_data(db: Session):
    education = DbTheme(name="education")
    db.add(education)
    history = DbTheme(name="history")
    db.add(history)
    sport = DbTheme(name="sport")
    db.add(sport)
    db.commit()
    db.refresh(education)
    db.refresh(history)
    db.refresh(sport)
    return "Ok"


async def get_themes(db: Session):
    themes = db.query(DbTheme).all()
    return themes


async def create_theme(request: ThemeInsert, db: Session):
    new_theme = DbTheme(name=request.name)
    db.add(new_theme)
    db.commit()
    db.refresh(new_theme)
    return new_theme
