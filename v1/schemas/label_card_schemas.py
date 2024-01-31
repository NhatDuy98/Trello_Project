from pydantic import BaseModel, Field, validator
from pydantic.alias_generators import to_camel
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.NAME_PATTERN

class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class LabelModel(ModelResponse):
    id: int = Field(..., gt = 0)
    label_name: str | None = Field(None, min_length = 1, max_length = 20)
    color: str = Field(..., min_length = 1, max_length = 100)

    @validator('label_name')
    @classmethod
    def validate_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('label name is invalid')
        return value

class LabelAdd(ModelResponse):
    id: int = Field(..., gt = 0)

class LabelCardModel(ModelResponse):
    id: int = Field(..., gt = 0)
    card_id: int = Field(..., gt = 0)
    label: LabelModel

class LabelCard(ModelResponse):
    data: list[LabelCardModel] = []