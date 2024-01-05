from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    expires: int