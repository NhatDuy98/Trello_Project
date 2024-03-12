from sqlalchemy.orm import Session
from v1.models.work_spaces import WorkSpace


def find_by_id(
    db: Session,
    id: int
):
    return db.query(WorkSpace).filter(WorkSpace.id == id).first()

def get_all_with_pagination(
        db: Session,
        user_id: int,
        page: int = 1,
        limit: int = 5,
        sort_by: str = None,
        sort_desc: bool = False,
        search: str = None
) -> list[WorkSpace]:
    
    offset = (page - 1) * limit

    db_query = db.query(WorkSpace).filter(WorkSpace.user_id == user_id)

    if search:
        db_query = db_query.filter(WorkSpace.work_space_name.ilike(f"%{search}%"))

    if sort_by:
        attr = getattr(WorkSpace, sort_by)
        db_query = db_query.order_by(
            attr.desc() if sort_desc else attr
        )
    
    total = db_query.count()

    work_spaces = db_query.offset(offset).limit(limit).all()

    return work_spaces, total

def count_all(db: Session):
    return db.query(WorkSpace).count()

def create_work_space(
    db: Session,
    work_space: WorkSpace
):
    db.add(work_space)
    db.commit()
    db.refresh(work_space)

    return work_space