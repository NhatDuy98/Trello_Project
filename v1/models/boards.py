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
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())
    deleted_at = Column(DateTime)
    work_space_id = Column(Integer, ForeignKey("work_spaces.id"), nullable = False)

    @classmethod
    def __snake_to_camel(cls, input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])
    
    def to_dto(self):
        result = {self.__snake_to_camel(key): getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_')}
        return result

    work_space = relationship("WorkSpace", back_populates = "boards")
    members = relationship("Member", back_populates = "board")
    # list_works = relationship("ListWork", back_populates = "board")
    # labels = relationship("Label", back_populates = "board")