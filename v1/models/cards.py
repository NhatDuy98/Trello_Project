from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from v1.models.utils import CamelCaseConverter

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    card_name = Column(String(45), nullable = False)
    description = Column(Text)
    is_delete = Column(Boolean, nullable = False, default = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())
    deleted_at = Column(DateTime)
    list_work_id = Column(Integer, ForeignKey("list_works.id"), nullable = False)

    def to_dto(self):
        return CamelCaseConverter.to_dto(self)

    list_work = relationship("ListWork", back_populates = 'cards')
    label_cards = relationship("LabelCard", back_populates = "card")