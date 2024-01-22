from sqlalchemy.orm import Session
from v1.models.list_works import ListWork

class ListWorkRepository:

    def __init__(self, db: Session, list_work: ListWork):
        self.db = db
        self.list_work = list_work

    def get_by_id(
        self,
        id: int
    ) -> ListWork:
        return self.db.query(self.list_work).filter(self.list_work.id == id).first()
    
    def get_all(
        self
    ) -> list[ListWork]:
        return self.db.query(self.list_work).all()
    
    async def save_list(
        self
    ):
        self.db.add(self.list_work)
        self.db.commit()
        self.db.refresh(self.list_work)