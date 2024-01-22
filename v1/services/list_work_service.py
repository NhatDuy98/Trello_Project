from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from v1.models import list_works, boards
from v1.repository import list_work_repo
from v1.schemas import list_work_schemas

class ListWorkService:
    def __init__(self, db: Session, list_work: list_works.ListWork):
        self.db = db
        self.list_work = list_work

    def get_all(
        self
    ):
        list_repo = list_work_repo.ListWorkRepository(self.db, self.list_work)

        lists = list_repo.get_all()

        data_response = list_work_schemas.ListWorkResponse(data = [list.to_dto() for list in lists])

        return data_response
    
    async def create_list(
        self,
        list_work: list_work_schemas.ListWorkCreate,
        board_id: int
    ):
        db_board = self.db.query(boards.Board).filter(boards.Board.id == board_id).first()

        if db_board is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
        if db_board.is_delete:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')

        try:
            list_db = self.list_work(**list_work.dict(), board_id = board_id)

            list_repo = list_work_repo.ListWorkRepository(self.db, list_db)

            await list_repo.save_list()

            return list_db.to_dto()
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create failed')
        
    
    async def update_list(
        self,
        board_id: int,
        list_id: int,
        list_work: list_work_schemas.ListWorkUpdate
    ):
        if not list_work.dict(exclude_unset = True):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'bad request')

        try:
            db_board = self.db.query(boards.Board).filter(boards.Board.id == board_id).first()
    
            if db_board.is_delete:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
        
        try:
            list_repo = list_work_repo.ListWorkRepository(self.db, self.list_work)

            list_db = list_repo.get_by_id(list_id)
    
            if list_db.is_delete:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
            
            for field in list_work.dict(exclude_unset = True):
                setattr(list_db, field, getattr(list_work, field))

            self.db.commit()
            self.db.refresh(list_db)
            
            return list_db.to_dto()
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'update failed')

    async def soft_delete(
        self,
        board_id: int,
        list_id: int
    ):
        db_board = self.db.query(boards.Board).filter(boards.Board.id == board_id).first()

        if db_board is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
        if db_board.is_delete:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        
        try:
            list_repo = list_work_repo.ListWorkRepository(self.db, self.list_work)

            list_db = list_repo.get_by_id(list_id)
    
            if list_db.is_delete:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
            
            list_db.is_delete = True
            list_db.deleted_at = datetime.now()

            self.db.commit()
            self.db.refresh(list_db)
            
            return list_db
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete failed')
