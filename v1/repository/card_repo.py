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

class CardRepository:
    def __init__(self, db: Session, card: Card):
        self.db = db
        self.card = card

    def get_by_id(
        self,
        id: int
    ) -> Card:
        return self.db.query(self.card).filter(self.card.id == id).first()
    
    def get_all(
        self,
        list_work_id: int
    ) -> list[Card]:
        return self.db.query(self.card).filter(self.card.list_work_id == list_work_id).all()
    
    async def create_card(
        self
    ):
        self.db.add(self.card)
        self.db.commit()
        self.db.refresh(self.card)

    async def save_card(
        self
    ):
        self.db.commit()
        self.db.refresh(self.card)