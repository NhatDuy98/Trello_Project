from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    board_name = Column(String(45), nullable = False)
    description = Column(String(255))
    is_delete = Column(Boolean, nullable = False, default = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, default = None, onupdate = datetime.now())
    deleted_at = Column(DateTime, default = None)
    work_space_id = Column(Integer, ForeignKey("work_spaces.id"))

    work_space = relationship("WorkSpace", back_populates = "boards")
    # members = relationship("Member", back_populates = "board")
    list_works = relationship("ListWork", back_populates = "board")
    labels = relationship("Label", back_populates = "board")