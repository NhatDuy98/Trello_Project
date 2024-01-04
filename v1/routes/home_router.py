from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.services import home_service
from v1.schemas.home_schemas import User, UserCreate
from v1.models import users

users.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1",
    tags = ["Home"],
    responses = {404: {"description": "Home not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/signup", response_model = User, status_code = status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        user: Annotated[UserCreate, Body(...)]
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