from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from v1.repository import label_repo, label_card_repo
from v1.schemas import label_schemas
from v1.services import label_card_service
from v1.models.labels import Label
from v1.models.boards import Board
from v1.models.label_cards import LabelCard

class LabelService:
    def __init__(self, db: Session, label: Label):
        self.db = db
        self.label = label

    def get_all(
        self,
        board_id: int
    ) -> label_schemas.LabelResponse:
        try:
            db_board = self.db.query(Board).filter(Board.id == board_id).first()

            if db_board is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
            if db_board.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        label_rp = label_repo.LabelRepository(db = self.db, label = self.label)
        
        db_label = label_rp.get_all(board_id = board_id)

        data_response = label_schemas.LabelResponse(data = [label.to_dto() for label in db_label])

        return data_response

    def get_by_id(
        self,
        label_id: int
    ):
        try:
            label_rp = label_repo.LabelRepository(db = self.db, label = self.label)

            label_db = label_rp.get_by_id(id = label_id)

            if label_db is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'label not found')

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        return label_db.to_dto()
    
    async def create_label(
        self,
        board_id: int,
        label: label_schemas.LabelCreate
    ):
        if not label.dict():
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            db_board = self.db.query(Board).filter(Board.id == board_id).first()

            if db_board is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
            if db_board.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            label_rp = label_repo.LabelRepository(db = self.db, label = self.label)

            labels_check = label_rp.get_all(board_id = board_id)

            for i in labels_check:
                if i.color == label.color and i.label_name == label.label_name:
                    raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'duplicate')
                
            db_label = self.label(**label.dict(), board_id = board_id)

            db_save = label_repo.LabelRepository(db = self.db, label = db_label)

            await db_save.save_label()

            return db_label.to_dto()

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create failed')
        
    async def update_label(
        self,
        board_id: int,
        label_id: int,
        label: label_schemas.LabelUpdate
    ):
        if not label.dict(exclude_unset = True):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            db_board = self.db.query(Board).filter(Board.id == board_id).first()

            if db_board is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
            if db_board.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            label_rp = label_repo.LabelRepository(db = self.db, label = self.label)

            labels_check = label_rp.get_all(board_id = board_id)

            for i in labels_check:
                if i.color == label.color and i.label_name == label.label_name:
                    raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'duplicate')
                
            db_label = label_rp.get_by_id(id = label_id)
                
            for field in label.dict(exclude_unset = True):
                setattr(db_label, field, getattr(label, field))

            label_save = label_repo.LabelRepository(db = self.db, label = db_label)

            await label_save.save_label()

            return db_label.to_dto()

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'update failed')

    
    async def delete_label(
        self,
        board_id: int,
        label_id: int
    ):
        try:
            db_board = self.db.query(Board).filter(Board.id == board_id).first()

            if db_board is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
            if db_board.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            label_card_rp = label_card_repo.LabelCardRepository(db = self.db, label_card = LabelCard)

            db_label_card = label_card_rp.get_all_with_label(label_id = label_id)

            label_card_sv = label_card_service.LabelCardService(db = self.db, label_card = LabelCard)

            for i in db_label_card:
                await label_card_sv.remove_label(card_id = i.card_id, label_card_id = i.id)

            label_rp = label_repo.LabelRepository(db = self.db, label = self.label)

            label_check = label_rp.get_by_id(id = label_id)

            if label_check:
                label_delete = label_repo.LabelRepository(db = self.db, label = label_check)

                await label_delete.delete_label()

            check_deleted = label_rp.get_by_id(id = label_id)

            if check_deleted:
                return False
            
            return True

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete failed')
