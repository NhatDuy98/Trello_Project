from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
# from v1.models.members import Member



class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    first_name = Column(String(20), nullable = False)
    last_name = Column(String(20), nullable = False)
    email = Column(String(20), unique = True, index = True)
    password = Column(String(100), nullable = False)
    is_active = Column(Boolean, nullable = False, default = True)
    is_delete = Column(Boolean, nullable = False, default = False)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())
    deleted_at = Column(DateTime)

    @classmethod
    def __camel_to_snake(cls, input_str: str) -> str:
        output_str = "".join(['_' + i.lower() if i.isupper() else i for i in input_str]).lstrip('_')
        return output_str

    @classmethod
    def __snake_to_camel(cls, input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])

    @classmethod
    def from_dto(cls, UserResponse):
        result = {cls.__camel_to_snake(key): value for key, value in UserResponse.dict().items()}
        return cls(**result)
    
    def to_dto(self):
        result = {self.__snake_to_camel(key): getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_') and hasattr(self, key)}
        return result

    work_spaces = relationship("WorkSpace", back_populates = "user")
    members = relationship("Member", back_populates = "user")