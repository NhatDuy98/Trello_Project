from sqlalchemy.orm import Session
from v1.models.list_works import ListWork

def get_by_id(
    db: Session,
    id: int
):
    return db.query(ListWork).filter(ListWork.id == id).first()

def get_all(
    db: Session,
):
    query = db.query(ListWork).all()
    return query

def count_all(
    db: Session
):
    return db.query(ListWork).count()