from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class LabelModel(ModelResponse):
    id: int = Field(..., gt = 0)
    label_name: str | None = Field(None, min_length = 1, max_length = 20)
    color: str = Field(..., min_length = 1, max_length = 100)

class LabelAdd(LabelModel):
    pass

class LabelCardModel(ModelResponse):
    id: int = Field(..., gt = 0)
    card_id: int = Field(..., gt = 0)
    label: LabelModel

class LabelCard(ModelResponse):
    data: list[LabelCardModel] = []