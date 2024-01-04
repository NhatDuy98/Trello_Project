from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.services import user_service
from v1.schemas.user_schemas import UserResponse
from v1.schemas.user_schemas import User, UserUpdate, UpdateAPart, UserUpdate, UserUpdateAPart
from v1.models import users

users.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1/users",
    tags = ["User"],
    responses = {404: {"description": "User not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("", response_model = UserResponse, status_code = status.HTTP_200_OK)
async def get_all_users(
    db: db_dependency,
    page: Annotated[int, Query()] = 1,
    limit: Annotated[int, Query] = 5,
    sort_by: Annotated[str, Query()] = None,
    sort_desc: Annotated[bool, Query()] = False,
    search: Annotated[str, Query()] = None,
    is_active: Annotated[bool, Query()] = None,
    is_delete: Annotated[bool, Query()] = None
):
    users = user_service.get_all_users(
        db = db,
        page = page,
        limit = limit,
        sort_by = sort_by,
        sort_desc = sort_desc,
        search = search,
        is_active = is_active,
        is_delete = is_delete
    )
    return users

@router.get('/{id}', response_model = User, status_code = status.HTTP_200_OK)
async def get_user_by_id(
    db: db_dependency,
    id: Annotated[int, Path(...)]
):
    user = user_service.get_user_by_id(db, id)

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")

    return user

@router.put('/{id}', response_model= User, status_code = status.HTTP_200_OK)
async def update_info_user(
    db: db_dependency,
    id: Annotated[int, Path(...)],
    user: Annotated[UserUpdate, Body(...)]
):
    user_email = user_service.find_user_by_email(db= db, email = user.email)

    if user_email:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "email already used")
    
    user_response = user_service.update_all_info_user(
        db = db,
        id = id,
        user = user
    )

    if user_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")
    
    return user_response

@router.patch('/{id}', response_model = UserUpdateAPart, status_code = status.HTTP_200_OK)
async def update_part_info_user(
    db: db_dependency,
    id: Annotated[int, Path(...)],
    user: Annotated[UpdateAPart, Body(...)]
):
    
    user_email = user_service.find_user_by_email(db, user.email)

    if user_email:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "email already used")

    user_response = user_service.update_part_info_user(
        db = db,
        id = id,
        user = user
    )

    if user_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")
    
    return user_response


@router.delete('/{id}', status_code = status.HTTP_200_OK)
async def soft_delete_user(
    db: db_dependency,
    id: Annotated[int, Path(...)]
):
    user = user_service.soft_delete_user(db, id)

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")

    return {"message": "delete user successfully"}