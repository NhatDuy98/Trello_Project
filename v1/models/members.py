from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

class RoleMemberEnum(enum.Enum):
    HOST = 'HOST'
    MEMBER = 'MEMBER'

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable = False)
    role = Column(Enum(RoleMemberEnum), default = RoleMemberEnum.MEMBER)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, server_default = func.now(), onupdate = datetime.now())

    @classmethod
    def __snake_to_camel(cls, input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])
    
    def to_dto(self):
        result = {self.__snake_to_camel(key): getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_')}
        return result

    user = relationship("User", back_populates = "members")
    board = relationship("Board", back_populates = "members")