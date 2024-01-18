from sqlalchemy.orm import Session
from v1.models.members import Member
from v1.models.users import User

class MemberRepository:

    def __init__(self, db: Session, member: Member):
        self.db = db
        self.member = member


    async def add_member(
        self
    ):
        self.db.add(self.member)
        self.db.commit()
        self.db.refresh(self.member)

    def get_all(
        self,
        board_id: int,
        search: str = None
    ) -> list[Member]:
        query = self.db.query(Member).outerjoin(User, self.member.user_id == User.id)

        if search:
            query = query.filter((User.email.ilike(f'%{search}%')))

        members = query.filter(self.member.board_id == board_id).all()

        return members
    
    def get_by_id(
        self,
        member_id: int
    ):
        return self.db.query(self.member).filter(self.member.id == member_id).first()
    
    def get_id_with_both(
        self,
        board_id: int,
        member_id: int
    ):
        return self.db.query(self.member).filter(self.member.board_id == board_id and self.member.id == member_id).first() 