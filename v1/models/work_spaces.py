from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class WorkSpace(Base):
    __tablename__ = 'work_spaces'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    work_space_name = Column(String(45), nullable = False)
    desciption = Column(String(255))
    is_delete = Column(Boolean, nullable = False, default = False)
    created_at = Column(DateTime, nullable = False, default = datetime.now())
    updated_at = Column(DateTime, nullable = False, default = datetime.now(), onupdate = datetime.now())
    deleted_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)

    @classmethod
    def __snake_to_camel(cls, input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])
    
    def to_dto(self):
        result = {self.__snake_to_camel(key): getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_')}
        return result

    user = relationship("User", back_populates = "work_spaces")
    boards = relationship("Board", back_populates = "work_space")