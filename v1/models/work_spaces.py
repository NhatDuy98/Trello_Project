from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class WorkSpace(Base):
    __tablename__ = 'work_spaces'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    work_space_name = Column(String(45), nullable = False)
    desciption = Column(String(255))
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, default = None, onupdate = datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # user = relationship("User", back_populates = "work_spaces")
    # boards = relationship("Board", back_populates = "work_space")