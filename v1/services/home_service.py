from v1.repository import home_repo
from sqlalchemy.orm import Session
from v1.schemas import home_schemas
from auth import auth_service
from v1.models.users import User
from datetime import datetime

def find_user_by_email(
    db: Session,
    email: str
):
    return home_repo.find_by_email(db, email)

def create_user(
        db: Session,
        user: home_schemas.UserCreate
) -> home_schemas.User:
    user.password = auth_service.get_password_hash(user.password)
    db_user = User.from_dto(user)

    user_created = home_repo.create_user(
        db = db,
        user = db_user
    )

    user_response = user_created.to_dto()       

    return user_response