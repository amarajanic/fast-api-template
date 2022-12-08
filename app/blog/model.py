from database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DbBlog(Base):
    __tablename__='blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("DbUser", back_populates="blogs")
    theme = relationship("DbTheme", back_populates="blogs")
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=False)
