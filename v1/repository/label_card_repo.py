from sqlalchemy.orm import Session
from v1.models.label_cards import LabelCard

class LabelCardRepository:
    def __init__(self, db: Session, label_card: LabelCard):
        self.db = db
        self.label_card = label_card

    def get_by_id(
        self,
        id: int
    ) -> LabelCard:
        return self.db.query(self.label_card).filter(self.label_card.id == id).first()
    
    def get_all(
        self,
        card_id: int
    ) -> list[LabelCard]:
        return self.db.query(self.label_card).filter(self.label_card.card_id == card_id).all()
    
    def get_all_with_label(
        self,
        label_id: int
    ) -> list[LabelCard]:
        return self.db.query(self.label_card).filter(self.label_card.label_id == label_id).all()
    
    async def save_label_card(
        self
    ):
        self.db.add(self.label_card)
        self.db.commit()
        self.db.refresh(self.label_card)

    async def delete_label_card(
        self
    ):
        self.db.delete(self.label_card)
        self.db.commit()
