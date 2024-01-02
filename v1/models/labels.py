from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from v1.models.boards import Board
from v1.models.label_cards import LabelCard

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    label_name = Column(String(20))
    color = Column(String(50), nullable = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, default = None, onupdate = datetime.now())
    board_id = Column(Integer, ForeignKey("boards.id"))

    # board = relationship("Board", back_populates = "labels")
    # label_cards = relationship("LabelCard", back_populates = "label")