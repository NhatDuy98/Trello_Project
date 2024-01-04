from v1.repository import user_repo
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from v1.schemas import user_schemas
from auth import auth_service
from v1.models.users import User
from datetime import datetime

def find_user_by_id(
    db: Session,
    id: int
) -> User:
    return user_repo.find_by_id(db, id)

def find_user_by_email(
    db: Session,
    email: str
) -> User:
    return user_repo.find_by_email(db, email)

def get_all_users(
    db: Session,
    page: int = 1,
    limit: int = 5,
    sort_by: str = None,
    sort_desc: bool = False,
    search: str = None,
    is_active: bool = None,
    is_delete: bool = None
) -> user_schemas.UserResponse:
    users = user_repo.get_all_users_with_pagination(
    db = db,
    page = page,
    limit = limit,
    sort_by = sort_by,
    sort_desc = sort_desc,
    search = search,
    is_active = is_active,
    is_delete = is_delete
    )
    total = user_repo.count_users(db)

    pagination = user_schemas.PaginationModel(
        page = page,
        limit = limit,
        totalRows = total
    )

    return user_schemas.UserResponse(
        data = [user.to_dto() for user in users],
        pagination = pagination
    )

def get_user_by_id(
    db: Session,
    id: int
) -> user_schemas.User:
    user = user_repo.find_by_id(
        db,
        id
    )
    return user.to_dto()

def update_all_info_user(
    db: Session,
    id: int,
    user: user_schemas.UserUpdate
) -> user_schemas.User:

    db_user = user_repo.find_by_id(db, id)

    if db_user.is_active is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user deleted can not update")

    for field in user.dict(exclude_unset=True):
        setattr(db_user, field, getattr(user, field))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user.to_dto()

def update_part_info_user(
    db: Session,
    id: int,
    user: user_schemas.UpdateAPart
) -> user_schemas.User:
    db_user = user_repo.find_by_id(db, id)

    if db_user.is_active is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user deleted can not update")

    for field in user.dict(exclude_unset=True):
        setattr(db_user, field, getattr(user, field))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user.to_dto()

def soft_delete_user(
    db: Session,
    id: int
) -> user_schemas.User:
    user = user_repo.find_by_id(db, id)

    if user.is_active is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user already deleted")

    user.is_delete = True
    user.is_active = False
    user.deleted_at = datetime.now()

    db.add(user)
    db.commit()
    db.refresh(user)

    return user.to_dto()
