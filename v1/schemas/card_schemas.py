from pydantic import BaseModel, Field, validator
from pydantic.alias_generators import to_camel
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.NAME_PATTERN

class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class CardModel(ModelResponse):
    card_name: str = Field(..., min_length = 1, max_length = 45)
    description: str | None = Field(None, min_length = 1, max_length = 455)

    @validator('card_name')
    @classmethod
    def validate_card_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('card name is invalid')
        return value

class CardCreate(CardModel):
    pass

class CardUpdate(ModelResponse):
    card_name: str = Field(None, min_length = 1, max_length = 45)
    description: str | None = Field(None, min_length = 1, max_length = 455)

    @validator('card_name')
    @classmethod
    def validate_card_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('card name is invalid')
        return value

class CardUpdated(CardUpdate):
    id: int = Field(..., gt = 0)
    list_work_id: int = Field(..., gt = 0)

class Card(CardModel):
    id: int = Field(..., gt = 0)
    list_work_id: int = Field(..., gt = 0)

class CardResponse(ModelResponse):
    data: list[Card] = []

class CardUpdateMove(ModelResponse):
    list_work_id: int = Field(..., gt = 0)

class CardUpdatedMove(CardUpdateMove):
    id: int = Field(..., gt = 0)