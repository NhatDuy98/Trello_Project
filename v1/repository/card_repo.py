from sqlalchemy.orm import Session
from v1.models.cards import Card

def get_by_id(
    db: Session,
    id: int
):
    return db.query(Card).filter(Card.id == id).first()

def get_all(
    db: Session
):
    return db.query(Card).all()