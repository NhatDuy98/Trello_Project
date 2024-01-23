from sqlalchemy.orm import Session
from v1.models.labels import Label

class LabelRepository:
    def __init__(self, db: Session, label: Label):
        self.db = db
        self.label = label

    def get_by_id(
        self,
        id: int
    ) -> Label:
        return self.db.query(self.label).filter(self.label.id == id).first()
    
    def get_all(
        self,
        board_id: int
    ) -> list[Label]:
        return self.db.query(self.label).filter(self.label.board_id == board_id).all()
    
    async def save_label(
        self
    ):
        self.db.add(self.label)
        self.db.commit()
        self.db.refresh(self.label)

    
    async def delete_label(
        self
    ):
        self.db.delete(self.label)
        self.db.commit()
