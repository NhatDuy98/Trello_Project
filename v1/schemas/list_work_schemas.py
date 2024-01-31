from pydantic import BaseModel, Field, validator
from pydantic.alias_generators import to_camel
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.NAME_PATTERN

class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class ListWorkModel(ModelResponse):
    list_work_name: str = Field(..., min_length = 1, max_length = 45)

    @validator('list_work_name')
    @classmethod
    def validate_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            return ValueError('list name is invalid')
        return value

class ListWorkCreate(ListWorkModel):
    pass

class ListWorkUpdate(ListWorkModel):
    pass

class ListWork(ListWorkModel):
    id: int = Field(..., gt = 0)
    board_id: int = Field(..., gt = 0)

class ListWorkResponse(ModelResponse):
    data: list[ListWork] = []