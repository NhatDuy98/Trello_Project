from fastapi import APIRouter, status, Depends, HTTPException, Body, Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
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
from core.config import get_settings, get_oath


settings = get_settings()
oauth = get_oath()

router = APIRouter(
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

    if user_response is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create failed')

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
    user: Annotated[str, Depends(auth_service.get_current_user)]
):
    return user

@router.get('/login', status_code = status.HTTP_200_OK)
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth', status_code = status.HTTP_200_OK)
async def auth_google(request: Request):
    try:
        response = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'authorize failed')
    
    user = response.get('userinfo')
    if user:
        request.session['user'] = dict(user)

    return RedirectResponse(url = '/')

@router.get('/logout', status_code = status.HTTP_200_OK)
async def logout_google(request: Request):
    request.session.pop('user')
    return RedirectResponse(url = '/')