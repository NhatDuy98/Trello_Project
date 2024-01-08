from fastapi import APIRouter, status, Depends, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.services import home_service
from v1.schemas import home_schemas
from v1.schemas import user_schemas
from v1.models import users
from fastapi.security import OAuth2PasswordRequestForm
from auth import auth_service
from datetime import timedelta
from auth.auth_schemas import TokenResponse
from core.config import get_settings

users.Base.metadata.create_all( bind = engine )

settings = get_settings()

router = APIRouter(
    prefix = "/api/v1",
    tags = ["Home"],
    responses = {404: {"description": "Home not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/signup", response_model = home_schemas.User, status_code = status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        user: Annotated[home_schemas.UserCreate, Body(...)]
):
    check_user_email = home_service.find_user_by_email(
        db = db,
        email = user.email
    )

    if check_user_email:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email already used")

    user_response = home_service.create_user(
        db = db,
        user = user
    )

    return user_response


@router.post('/token', response_model = TokenResponse, status_code = status.HTTP_201_CREATED)
async def login_to_get_token(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    db_user = auth_service.authenticate_user(db, form_data)

    access_token_expies = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        user = db_user,
        expires_delta = access_token_expies
    )
    return access_token


@router.get('/me', response_model = user_schemas.User, status_code = status.HTTP_200_OK)
async def login(
    user: Annotated[users.User, Depends(auth_service.get_current_user)]
):
    return user
