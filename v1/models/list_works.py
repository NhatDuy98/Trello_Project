from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class ListWork(Base):
    __tablename__ = 'list_works'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    list_work_name = Column(String(45), nullable = False)
    is_delete = Column(Boolean, nullable = False, default = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, default = None, onupdate = datetime.now())
    deleted_at = Column(DateTime, default = None)
    board_id = Column(Integer, ForeignKey("boards.id"))

    board = relationship("Board", back_populates = "list_works")
    cards = relationship("Card", back_populates = 'list_work')