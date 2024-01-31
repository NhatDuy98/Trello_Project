from pydantic import BaseModel, Field, validator
from pydantic.alias_generators import to_camel
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.NAME_PATTERN

class BaseResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class LabelModel(BaseResponse):
    label_name: str | None = Field(None, min_length = 1, max_length = 20)
    color: str = Field(..., min_length = 1, max_length = 100)

    @validator('label_name')
    @classmethod
    def validate_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('label name is invalid')
        return value

class LabelCreate(LabelModel):
    pass

class LabelUpdate(BaseResponse):
    label_name: str | None = Field(None, min_length = 1, max_length = 20)
    color: str = Field(None, min_length = 1, max_length = 100)

    @validator('label_name')
    @classmethod
    def validate_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('label name is invalid')
        return value

class LabelUpdated(LabelUpdate):
    id: int = Field(..., gt = 0)
    board_id: int = Field(..., gt = 0)

class Label(LabelModel):
    id: int = Field(..., gt = 0)
    board_id: int = Field(..., gt = 0)

class LabelResponse(BaseResponse):
    data: list[Label] = []