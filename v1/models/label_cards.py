from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from v1.models.labels import Label
from v1.models.cards import Card

class LabelCard(Base):
    __tablename__ = 'label_cards'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    label_id = Column(Integer, ForeignKey("labels.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, default = None, onupdate = datetime.now())

    # label = relationship("Label", back_populates= "label_cards")
    # card = relationship("Card", back_populates = "label_cards")