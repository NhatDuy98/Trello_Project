from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from v1.repository import label_card_repo, label_repo, card_repo
from v1.schemas import label_card_schemas
from v1.models.label_cards import LabelCard
from v1.models.list_works import ListWork
from v1.models.labels import Label

class LabelCardService:
    def __init__(self, db: Session, label_card: LabelCard):
        self.db = db
        self.label_card = label_card

    async def add_label_to_card(
        self,
        board_id: int,
        list_work_id: int,
        card_id: int,
        label: label_card_schemas.LabelAdd
    ):
        label_rp = label_repo.LabelRepository(db = self.db, label = Label)

        db_label = label_rp.get_by_id(id = label.id)

        if db_label is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'label not found')
    
        if db_label.board_id != board_id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not add label in another board')
        
        db_list_work = self.db.query(ListWork).filter(ListWork.id == list_work_id).first()

        if db_list_work is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')

        if db_list_work.board_id != board_id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not add label in another board')

        try:
            label_card_rp = label_card_repo.LabelCardRepository(db = self.db, label_card = LabelCard)

            label_check = label_card_rp.get_all(card_id = card_id)

            for i in label_check:
                if i.label_id == label.id:
                    raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'duplicate')

            db_label_card = LabelCard(card_id = card_id, label_id = label.id)

            label_save = label_card_repo.LabelCardRepository(db = self.db, label_card = db_label_card)

            await label_save.save_label_card()

            return db_label_card
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'add failed')
        
    async def remove_label(
        self,
        card_id: int,
        label_card_id: int
    ):
        db_card = card_repo.get_by_id(db = self.db, id = card_id)

        if db_card is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')

        try:
            label_card_rp = label_card_repo.LabelCardRepository(db = self.db, label_card = LabelCard)

            db_label_card = label_card_rp.get_by_id(id = label_card_id)

            db_delete = label_card_repo.LabelCardRepository(db = self.db, label_card = db_label_card)

            await db_delete.delete_label_card()

            label_card_check = label_card_rp.get_by_id(id = label_card_id)

            if label_card_check:
                return False

            return True
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'remove failed')
