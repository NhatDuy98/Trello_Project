from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from v1.models.utils import CamelCaseConverter
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
    created_at = Column(DateTime, nullable = False, default = datetime.now())
    updated_at = Column(DateTime, nullable = False, default = datetime.now(), onupdate = datetime.now())
    
    def to_dto(self):
        return CamelCaseConverter.to_dto(self)

    user = relationship("User", back_populates = "members")
    board = relationship("Board", back_populates = "members")