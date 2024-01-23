from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class LabelCard(Base):
    __tablename__ = 'label_cards'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable = False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())

    @classmethod
    def __snake_to_camel(cls, input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])
    
    def to_dto(self):
        result = {self.__snake_to_camel(key): getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_') and hasattr(self, key)}
        return result

    label = relationship("Label", back_populates= "label_cards")
    card = relationship("Card", back_populates = "label_cards")