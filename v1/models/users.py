from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    first_name = Column(String(20), nullable = False)
    last_name = Column(String(20), nullable = False)
    email = Column(String(20), unique = True, index = True)
    password = Column(String(100), nullable = False)
    is_active = Column(Boolean, nullable = False, default = True)
    is_delete = Column(Boolean, nullable = False, default = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, default = None, onupdate = datetime.now())
    deleted_at = Column(DateTime)

    work_spaces = relationship("WorkSpace", back_populates = "user")
    members = relationship("Member", back_populates = "user")