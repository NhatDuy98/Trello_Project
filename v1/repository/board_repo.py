from sqlalchemy.orm import Session
from v1.models.boards import Board
from v1.models.members import Member

class BoardRepository:
    def __init__(self, db: Session, board: Board):
        self.db = db
        self.board = board

    def get_by_id(
        self,
        id: int
    ) -> Board:
        return self.db.query(self.board).filter(self.board.id == id).first()
    
    def get_all(
        self,
        work_space_id: int,
        page: int = 1,
        limit: int = 5,
        sort_by: str = None,
        sort_desc: bool = False,
        search: str = None
    ) -> list[Board]:
        offset = (page - 1) * limit

        query = self.db.query(self.board).filter(self.board.work_space_id == work_space_id)

        if search:
            query = query.filter(self.board.board_name.ilike(f'%{search}%'))

        if sort_by:
            attr = getattr(Board, sort_by)
            query = query.order_by(attr.desc() if sort_desc else attr)

        total = query.count()

        boards = query.offset(offset).limit(limit).all()
        
        return boards, total
    
    def count_all(
        self
    ) -> int:
        return self.db.query(self.board).count()
    
    async def create_member(
        self,
        member: Member
    ):
        self.db.add(member)
        self.db.commit()
        # self.db.refresh(member)
    
    async def create_board_and_member(
        self,
        member: Member
    ):
        self.db.add_all([self.board, member])
        self.db.commit()
        self.db.refresh(self.board)
