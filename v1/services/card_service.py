from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from v1.repository import card_repo
from v1.schemas import card_schemas
from v1.models.cards import Card
from v1.models.boards import Board
from v1.models.list_works import ListWork


class CardService:
    def __init__(self, db: Session, card: Card):
        self.db = db
        self.card = card

    def get_all(
        self,
        list_work_id: int
    ):
        card_rp = card_repo.CardRepository(db = self.db, card = self.card)

        cards = card_rp.get_all(list_work_id = list_work_id)

        card_response = card_schemas.CardResponse(data = [card.to_dto() for card in cards])

        return card_response
    
    async def create_card(
        self,
        list_work_id: int,
        card: card_schemas.CardCreate
    ):
        if not card.dict():
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            db_list = self.db.query(ListWork).filter(ListWork.id == list_work_id).first()

            if db_list is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
            if db_list.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'system error')
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            for field in card.dict(exclude_unset = True):
                field_value = getattr(card, field)
                if isinstance(field_value, str):
                    setattr(card, field, field_value.strip())

            db_card = Card(**card.dict(), list_work_id = list_work_id)

            card_rp = card_repo.CardRepository(db = self.db, card = db_card)

            await card_rp.create_card()

            return db_card.to_dto()

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create failed')
        
    async def update_card(
        self,
        list_id: int,
        card_id: int,
        card: card_schemas.CardUpdate
    ):
        try:
            if not card.dict(exclude_unset = True):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

            db_list = self.db.query(ListWork).filter(ListWork.id == list_id).first()

            if db_list is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
            if db_list.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            card_rp = card_repo.CardRepository(db = self.db, card = self.card)

            db_card = card_rp.get_by_id(id = card_id)

            if db_card is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')
    
            if db_card.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
            if db_card.list_work_id != list_id:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
            
            for field in card.dict(exclude_unset = True):
                field_value = getattr(card, field)
                if isinstance(field_value, str):
                    setattr(db_card, field, field_value.strip())
                else:
                    setattr(db_card, field, field_value)

            card_save = card_repo.CardRepository(db = self.db, card = db_card)

            await card_save.save_card()

            return db_card.to_dto()

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'update failed')


    async def soft_delete(
        self,
        list_id: int,
        card_id: int
    ):
        try:
            db_list = self.db.query(ListWork).filter(ListWork.id == list_id).first()

            if db_list is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
            if db_list.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
            
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        try:
            card_rp = card_repo.CardRepository(db = self.db, card = self.card)

            db_card = card_rp.get_by_id(id = card_id)

            if db_card is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')
    
            if db_card.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
            if db_card.list_work_id != list_id:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
            
            db_card.is_delete = True
            db_card.deleted_at = datetime.now()

            db_save = card_repo.CardRepository(db = self.db, card = db_card)

            await db_save.save_card()

            return db_card
            
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete failed')
        
    async def update_action_move_card(
        self,
        card_id: int,
        list: card_schemas.CardUpdateMove
    ):
        try:
            db_list = self.db.query(ListWork).filter(ListWork.id == list.list_work_id).first()

            if db_list is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
            if db_list.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
            
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

        try:
            card_rp = card_repo.CardRepository(db = self.db, card = self.card)

            db_card = card_rp.get_by_id(id = card_id)

            if db_card is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')
    
            if db_card.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
            
            db_card.list_work_id = list.list_work_id

            card_save = card_repo.CardRepository(db = self.db, card = db_card)

            await card_save.save_card()

            return db_card
            
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'move failed')