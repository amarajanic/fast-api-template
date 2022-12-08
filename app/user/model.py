from database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from role.model import DbRole


class DbUser(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    blogs = relationship("DbBlog", back_populates="user", uselist=True)
    role = relationship("DbRole", back_populates="users")

