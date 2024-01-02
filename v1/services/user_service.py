from v1.repository import user_repo
from sqlalchemy.orm import Session
from v1.schemas import user_schemas
from auth import auth_service
from v1.models.users import User
from datetime import datetime

def find_user_by_id(
    db: Session,
    id: int
):
    return user_repo.find_by_id(db, id)

def find_user_by_email(
    db: Session,
    email: str
):
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

def create_user(
        db: Session,
        user: user_schemas.UserCreate
) -> user_schemas.User:
    user.password = auth_service.get_password_hash(user.password)
    db_user = User.from_dto(user)

    user_created = user_repo.create_user(
        db = db,
        user = db_user
    )

    user_response = user_created.to_dto()

    return user_response

