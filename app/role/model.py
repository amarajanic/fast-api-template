from database.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class DbRole(Base):
    __tablename__='roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("DbUser", back_populates="role", uselist=True)
