from database.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class DbTheme(Base):
    __tablename__='themes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    blogs = relationship("DbBlog", back_populates="theme", uselist=True)
