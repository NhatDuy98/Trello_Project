from pydantic import BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel

class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class UserModel(ModelResponse):
    id: int = Field(...)
    email: EmailStr = Field(...)

class UserAdd(UserModel):
    pass

class MemberModel(ModelResponse):
    id: int = Field(...)
    role: str = Field(...)
    user: UserModel

class Member(BaseModel):
    data: list[MemberModel] = []