from pydantic import BaseModel, Field, EmailStr
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class PaginationModel(BaseModel):
    page: int = Field(None)
    limit: int = Field(None)
    totalRows: int = Field(None)

class UserModel(CamelCaseModel):
    first_name: str = Field(..., min_length= 1, max_length = 30, description = "must have 1 to 30 characters")
    last_name: str = Field(..., max_length = 30, description = "last name have at most 30 characters")
    email: EmailStr = Field(..., max_length = 25, description = "email have at most 25 characters")

class UserCreate(UserModel):
    password: str = Field(..., min_length = 6, max_length = 18, description = "must have 6 to 18 characters")

class UserUpdate(UserModel):
    pass

class User(UserModel):
    id: int = Field(..., gt = 0)
    is_active: bool = Field(True)

class UpdateAPart(CamelCaseModel):
    first_name: str = Field(None, min_length = 1, max_length = 30, description = "must have 1 to 30 characters")
    last_name: str = Field(None, max_length = 30, description = "last name have at most 30 characters")
    email: EmailStr = Field(None, max_length = 25, description = "email have at most 25 characters")

class UserUpdateAPart(UpdateAPart):
    id: int = Field(..., gt = 0)
    is_active: bool = Field(True)
    

class UserResponse(BaseModel):
    data: list[User] = []
    pagination: PaginationModel