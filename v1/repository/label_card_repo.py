from sqlalchemy.orm import Session
from v1.models.label_cards import LabelCard


def get_by_id(
    db: Session,
    id: int
):
    return db.query(LabelCard).filter(LabelCard.id == id).first()

def get_all(
    db: Session,
    card_id: int
):
    return db.query(LabelCard).filter(LabelCard.card_id == card_id).all()

def get_all_with_label(
    db: Session,
    label_id: int
):
    return db.query(LabelCard).filter(LabelCard.label_id == label_id).all()