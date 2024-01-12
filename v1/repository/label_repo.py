from sqlalchemy.orm import Session
from v1.models.labels import Label

def get_by_id(
    db: Session,
    id: int
):
    return db.query(Label).filter(Label.id == id).first()

def get_all(
    db: Session,
    board_id: int
):
    query = db.query(Label).filter(Label.board_id == board_id).all()

    return query