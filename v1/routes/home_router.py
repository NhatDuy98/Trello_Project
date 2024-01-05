from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth import auth_service
from core.database import get_db
from datetime import timedelta
from auth.auth_schemas import TokenResponse
from v1.schemas import user_schemas
from v1.models.users import User

ACCESS_TOKEN_EXPIRES_MINUTES = 30

router = APIRouter(
    prefix = "/api/v1",
    tags = ["Home"],
    responses = {404: {"description": "Home not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/token', response_model = TokenResponse, status_code = status.HTTP_201_CREATED)
async def login_to_get_token(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    db_user = auth_service.authenticate_user(db, form_data)

    access_token_expies = timedelta(minutes = ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = auth_service.create_access_token(
        user = db_user,
        expires_delta = access_token_expies
    )
    return access_token

@router.get('/me', response_model = user_schemas.User, status_code = status.HTTP_200_OK)
async def login(
    user: Annotated[User, Depends(auth_service.get_current_user)]
):
    return user