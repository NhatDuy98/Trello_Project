from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from auth.auth_service import return_current_user
from core.database import get_db
from core.config import get_settings
from sqlalchemy.orm import Session
from typing import Annotated
from v1.services import user_service
from v1.schemas.user_schemas import UserResponse
from v1.schemas.user_schemas import User, UserUpdate, UpdateAPart, UserUpdate, UserUpdateAPart
from v1.models import users

settings = get_settings()

user_ep = settings.END_POINT_USER


router = APIRouter(
    prefix = f'/{user_ep}',
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

@router.put('', response_model= User, status_code = status.HTTP_201_CREATED)
async def update_info_user(
    db: db_dependency,
    id: Annotated[int, Depends(return_current_user)],
    user: Annotated[UserUpdate, Body(...)]
):
    user_response = user_service.update_all_info_user(
        db = db,
        id = id,
        user = user
    )

    if user_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")
    
    return user_response

@router.patch('', response_model = UserUpdateAPart, status_code = status.HTTP_201_CREATED)
async def update_part_info_user(
    db: db_dependency,
    id: Annotated[int, Depends(return_current_user)],
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


@router.delete('', status_code = status.HTTP_204_NO_CONTENT)
async def soft_delete_user(
    db: db_dependency,
    id: Annotated[int, Depends(return_current_user)]
):
    user = user_service.soft_delete_user(db, id)

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")

    return {"message": "delete user successfully"}