from pydantic import BaseModel, Field, validator
from datetime import datetime
from pydantic.alias_generators import to_camel
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.NAME_PATTERN

class ModelConfig(BaseModel):
    class Config:
        from_attributes = True
        alias_generator = to_camel

class PaginationModel(BaseModel):
    page: int = Field(..., gt = 0)
    limit: int = Field(..., gt = 0)
    totalRows: int

class WorkSpaceModel(ModelConfig):
    work_space_name: str = Field(..., min_length = 1, max_length = 45, description = "name must have 1 to 45 characters")
    desciption: str | None = Field(None, max_length = 255, description = "too long")

    @validator('work_space_name')
    @classmethod
    def validate_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('work space name is invalid')
        return value

class WorkSpaceCreate(WorkSpaceModel):
    pass

class WorkSpace(WorkSpaceModel):
    id: int = Field(..., gt = 0)
    user_id: int = Field(..., gt = 0)


class WorkSpaceResponse(BaseModel):
    data: list[WorkSpace] = []
    pagination: PaginationModel