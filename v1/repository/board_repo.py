from sqlalchemy.orm import Session
from v1.models.boards import Board

def get_by_id(
    db: Session,
    id: int
) -> Board:
    return db.query(Board).filter(Board.id == id).first()

def get_all(
    db: Session,
    page: int = 1,
    limit: int = 5,
    sort_by: str = None,
    sort_desc: bool = False,
    search: str = None
) -> list[Board]:
    offset = ( page - 1 ) * limit

    query = db.query(Board)

    if search:
        query = query.filter(Board.board_name.ilike(f'%{search}%'))

    if sort_by:
        attr = getattr(Board, sort_by)
        query = query.order_by(attr.desc() if sort_desc else attr)

    boards = query.offset(offset).limit(limit).all()


    return boards

def count_all(
    db: Session
) -> int:
    return db.query(Board).count()