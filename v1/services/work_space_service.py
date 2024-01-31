from v1.repository import work_space_repo
from sqlalchemy.orm import Session
from v1.schemas import work_space_schemas
from v1.models.work_spaces import WorkSpace
from datetime import datetime
from v1.services import user_service
from fastapi import HTTPException, status


def get_work_space_by_id(
    db: Session,
    id: int
):
    work_space = work_space_repo.find_by_id(db, id)
    return work_space

def get_all_with_pagination(
        db: Session,
        page: int = 1,
        limit: int = 5,
        sort_by: str = None,
        sort_desc: bool = False,
        search: str = None
) -> work_space_schemas.WorkSpaceResponse:
    try:
        if page <= 0 or limit <= 0:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        if sort_by not in WorkSpace.__dict__ and sort_by is not None:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

        work_spaces, total = work_space_repo.get_all_with_pagination(
            db = db,
            page = page,
            limit = limit,
            sort_by = sort_by,
            sort_desc = sort_desc,
            search = search
        )

        pagination = work_space_schemas.PaginationModel(
            page = page,
            limit = limit,
            totalRows = total
        )

        return work_space_schemas.WorkSpaceResponse(
            data = [i.to_dto() for i in work_spaces],
            pagination = pagination
        )
    except HTTPException:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

def create_work_space(
    db: Session,
    user_id: int,
    work_space: work_space_schemas.WorkSpaceCreate
):
    if not work_space.dict(exclude_unset = True):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    db_user = user_service.find_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')
    
    if db_user.is_active is False:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'user not allow')
    
    for field in work_space.dict(exclude_unset = True):
        field_value = getattr(work_space, field)
        if isinstance(field_value, str):
            setattr(work_space, field, field_value.strip())

    db_work_space = WorkSpace(**work_space.dict(), user_id = user_id)

    work_space_response = work_space_repo.create_work_space(
        db = db,
        work_space = db_work_space
    )
    return work_space_response.to_dto()

def soft_delete_work_space(db: Session, user_id: int, work_space_id: int):
    db_work_space = work_space_repo.find_by_id(db, work_space_id)

    if db_work_space is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "work space not found")
    
    if db_work_space.user_id != user_id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'user not allow')
    
    if db_work_space:
        db_work_space.is_delete = True
        db_work_space.deleted_at = datetime.now()

        db.add(db_work_space)
        db.commit()

        return db_work_space