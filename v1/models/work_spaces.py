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
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())
    deleted_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)

    @classmethod
    def __camel_to_snake(cls, input_str: str) -> str:
        output_str = "".join(['_' + i.lower() if i.isupper() else i for i in input_str]).lstrip('_')
        return output_str

    @classmethod
    def __snake_to_camel(cls, input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])

    @classmethod
    def from_dto(cls, PydanticModel):
        result = {cls.__camel_to_snake(key): value for key, value in PydanticModel.dict().items()}
        return cls(**result)
    
    def to_dto(self):
        result = {self.__snake_to_camel(key): getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_')}
        return result

    user = relationship("User", back_populates = "work_spaces")
    # boards = relationship("Board", back_populates = "work_space")