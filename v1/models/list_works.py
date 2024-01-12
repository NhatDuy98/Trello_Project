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
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())
    deleted_at = Column(DateTime)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable = False)

    @classmethod
    def __snake_to_camel(cls, input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])
    
    def to_dto(self):
        result = {self.__snake_to_camel(key): getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_') and hasattr(self, key)}
        return result

    board = relationship("Board", back_populates = "list_works")
    # cards = relationship("Card", back_populates = 'list_work')