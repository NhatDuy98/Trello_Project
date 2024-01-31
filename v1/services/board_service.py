from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from v1.repository import board_repo, member_repo
from v1.schemas import board_schemas
from v1.models import boards, members
from v1.services import user_service, work_space_service

board_model = boards.Board

class BoardService:

    def __init__(self, db: Session, board: boards.Board):
        self.db = db
        self.board = board
    

    def get_by_id(
        self,
        id: int
    ):
        try:
            board_rp = board_repo.BoardRepository(self.db, self.board)

            board = board_rp.get_by_id(id)

            if board:
                return board.to_dto()

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')

    def get_all(
        self,
        page: int = 1,
        limit: int = 5,
        sort_by: str = None,
        sort_desc: bool = False,
        search: str = None
    ):
        try:
            if page <= 0 or limit <= 0:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
            if sort_by not in board_model.__dict__ and sort_by is not None:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

            board_repos = board_repo.BoardRepository(self.db, self.board)

            boards, total = board_repos.get_all(
                page = page,
                limit = limit,
                sort_by = sort_by,
                sort_desc = sort_desc,
                search = search
            )

            pagination = board_schemas.PaginationModel(page = page, limit = limit, totalRows = total)

            return board_schemas.BoardResponse(data = [board.to_dto() for board in boards], pagination = pagination)
        
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
    
    async def create_board(
        self,
        user_id: int,
        work_space_id: int,
        board_create: board_schemas.BoardCreate
    ):
        if not board_create.dict(exclude_unset = True):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        db_user = user_service.find_user_by_id(self.db, user_id)

        if db_user is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')
    
        if db_user.is_active is False:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')

        db_work_space = work_space_service.get_work_space_by_id(self.db, work_space_id)

        if db_work_space is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'work space not found')
    
        if db_work_space.is_delete:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        
        try:
            for field in board_create.dict(exclude_unset=True):
                field_value = getattr(board_create, field)
                if isinstance(field_value, str):
                    setattr(board_create, field, field_value.strip())

            board_save = boards.Board(**board_create.dict(), work_space_id = work_space_id)
        
            db_board = board_repo.BoardRepository(self.db, board_save)

            await db_board.create_board()

            db_member = members.Member(user_id = user_id, board_id = board_save.id, role = 'HOST')

            member_save = member_repo.MemberRepository(self.db, db_member)

            member_save.add_member() #check code with await

            return board_save.to_dto()
        
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create fail')
        
    def update_board(
        self,
        id: int,
        board_update: board_schemas.BoardUpdate
    ):
        if not board_update.dict(exclude_unset = True):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
        
        board = board_repo.BoardRepository(self.db, self.board)

        db_board = board.get_by_id(id)

        if db_board is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
        
        if db_board.is_delete:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'can not update board deleted')

        try:
            for field in board_update.dict(exclude_unset=True):
                field_value = getattr(board_update, field)
                if isinstance(field_value, str):
                    setattr(db_board, field, field_value.strip())
                else:
                    setattr(db_board, field, field_value)

            self.db.commit()
            self.db.refresh(db_board)

            return db_board.to_dto()
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'update fail')
        
    
    def soft_delete(
        self,
        id: int
    ):
        board_rp = board_repo.BoardRepository(self.db, self.board)

        db_board = board_rp.get_by_id(id = id)

        if db_board is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
        
        if db_board.is_delete:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
        
        try:
            db_board.is_delete = True
            db_board.deleted_at = datetime.now()

            self.db.commit()
            self.db.refresh(db_board)

            return db_board
        
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete fail')
