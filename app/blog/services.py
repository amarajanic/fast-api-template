from blog.schemas import BlogInsert, BlogUpdate, OrderBy
from sqlalchemy.orm import Session
from blog.model import DbBlog
from fastapi import HTTPException, status
from blog.fetch import fetch_blogs
from user.model import DbUser
from random import randint
from sqlalchemy import desc, asc


async def create_blog(request: BlogInsert, db: Session):
    new_blog = DbBlog(title=request.title, body=request.body,
                      user_id=request.user_id, theme_id=request.theme_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


async def get_blogs(db: Session, search: str, order_by: OrderBy, skip: int = 0, limit: int = 100):
    order_dict = {"OrderBy.az": asc(
        DbBlog.title), "OrderBy.za": desc(DbBlog.title)}

    if search:
        blogs = db.query(DbBlog).filter(DbBlog.title.ilike(f"%{search}%"))
    else:
        blogs = db.query(DbBlog)

    blogs = blogs.order_by(order_dict.get(str(order_by)))

    blogs = blogs.offset(skip).limit(limit).all()
    return blogs


async def get_blog_by_id(id: int, db: Session):
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    return blog


async def delete_blog(id: int, db: Session):
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()
    return blog


async def update_blog(id: int, request: BlogUpdate, db: Session):
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog = db.query(DbBlog).filter(DbBlog.id == id)
    blog.update({
        DbBlog.title: request.title,
        DbBlog.body: request.body,
        DbBlog.user_id: request.user_id,
        DbBlog.theme_id: request.theme_id
    })
    db.commit()
    return f"Blog with id {id} updated."


async def sync_blogs(db: Session):
    # try:
    blogs = await fetch_blogs()
    dbBlogs = []
    users_count = db.query(DbUser).count()
    for index, blog in enumerate(blogs["entries"]):
        if index == 200:
            break
        new_blog = DbBlog(
            title=blog["API"],
            body=blog["Description"],
            user_id=randint(1, users_count),
            theme_id=1
        )
        dbBlogs.append(new_blog)
    db.bulk_save_objects(dbBlogs)
    db.commit()
    return {"detail": "Synced successfully"}
    # except:
    #    db.rollback()
    #    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Failed to sync with external API")
