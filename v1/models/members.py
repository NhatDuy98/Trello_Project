from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class RoleMemberEnum(str, Enum):
    HOST = 'HOST'
    MEMBER = 'MEMBER'

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    board_id = Column(Integer, ForeignKey("boards.id"))
    role = Column(Enum(RoleMemberEnum), default = RoleMemberEnum.MEMBER)
    created_at = Column(DateTime, nullable = False, server_default = func.now())
    updated_at = Column(DateTime, nullable = False, default = None, onupdate = datetime.now())

    user = relationship("User", back_populates = "members")
    board = relationship("Board", back_populates = "members")