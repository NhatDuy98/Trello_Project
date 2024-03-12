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

    try:
        if page <= 0 or limit <= 0:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        if sort_by not in User.__dict__ and sort_by is not None:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')


        users, total = user_repo.get_all_users_with_pagination(
            db = db,
            page = page,
            limit = limit,
            sort_by = sort_by,
            sort_desc = sort_desc,
            search = search,
            is_active = is_active,
            is_delete = is_delete
        )

        pagination = user_schemas.PaginationModel(
            page = page,
            limit = limit,
            totalRows = total
        )

        return user_schemas.UserResponse(
            data = [user.to_dto() for user in users],
            pagination = pagination
        )
            
    except HTTPException:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

def get_user_by_id(
    db: Session,
    id: int
) -> user_schemas.User:
    try:
        user = user_repo.find_by_id(
            db,
            id
        )
        if user:
            return user.to_dto()

    except HTTPException:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')

def update_all_info_user(
    db: Session,
    id: int,
    user: user_schemas.UserUpdate
) -> user_schemas.User:
    
        
        if not user.dict(exclude_unset = True):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

        db_user = user_repo.find_by_id(db, id)

        if db_user is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')

        if db_user.is_active is False:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user deleted can not update")
        
        if user.email and user.email != db_user.email:
            user_email = find_user_by_email(db = db, email = user.email)
            if user_email:
                raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'email already used')

        for field in user.dict(exclude_unset=True):
            field_value = getattr(user, field)
            if isinstance(field_value, str):
                setattr(db_user, field, field_value.strip())
            else:
                setattr(db_user, field, field_value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user.to_dto()
    
    

def update_part_info_user(
    db: Session,
    id: int,
    user: user_schemas.UpdateAPart
) -> user_schemas.User:
    
    if not user.dict(exclude_unset = True):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    try:
        db_user = user_repo.find_by_id(db, id)

        if db_user:
            if db_user.is_active is False:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user deleted can not update")

            for field in user.dict(exclude_unset=True):
                field_value = getattr(user, field)
                if isinstance(field_value, str):
                    setattr(db_user, field, field_value.strip())
                else:
                    setattr(db_user, field, field_value)

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return db_user.to_dto()
    except HTTPException:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'update failed')

def soft_delete_user(
    db: Session,
    id: int
) -> user_schemas.User:
    try:
        user = user_repo.find_by_id(db, id)

        if user:
            if user.is_active is False:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "user already deleted")

            user.is_delete = True
            user.is_active = False
            user.deleted_at = datetime.now()

            db.add(user)
            db.commit()
            db.refresh(user)

            return user.to_dto()
    except HTTPException:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete failed')

    
