from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from v1.models.utils import CamelCaseConverter

class LabelCard(Base):
    __tablename__ = 'label_cards'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable = False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())

    def to_dto(self):
        return CamelCaseConverter.to_dto(self)

    label = relationship("Label", back_populates= "label_cards")
    card = relationship("Card", back_populates = "label_cards")