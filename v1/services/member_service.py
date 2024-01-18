from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from v1.models.members import Member
from v1.schemas import member_schemas
from v1.repository import member_repo
from v1.services import user_service, board_service
from v1.models import members

class MemberService:
    def __init__(self, db: Session, member: Member):
        self.db = db
        self.member = member

    def get_all(
        self,
        board_id: int,
        search: str = None
    ):
        member = member_repo.MemberRepository(self.db, self.member)

        db_members = member.get_all(board_id = board_id, search = search)

        member_response = []

        for i in db_members:
            db_user = user_service.find_user_by_id(self.db, i.user_id)
            user = member_schemas.UserModel(id = i.user_id, email = db_user.email)

            member_out = member_schemas.MemberModel(id = i.id, role = i.role, user = user)

            member_response.append(member_out)

        return member_schemas.Member(data = member_response)

    async def add_member(
        self,
        board_id: int,
        user: member_schemas.UserAdd
    ):
        member = member_repo.MemberRepository(self.db, self.member)

        db_member = member.get_all(board_id = board_id)

        db_user = user_service.find_user_by_id(self.db, user.id)

        if db_user.email != user.email:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'email wrong')

        for i in db_member:
            if i.user_id == user.id:
                raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'user already in group')
        
            if i.user_id == user.id and i.role == members.RoleMemberEnum.HOST:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')

        try:
            member_save = Member(user_id = user.id, board_id = board_id)

            member_rp = member_repo.MemberRepository(self.db, member_save)

            await member_rp.add_member()

            return member
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'add member fail')
        
    def remove_member(
        self,
        board_id: int,
        member_id: int
    ):
        member = member_repo.MemberRepository(self.db, self.member)

        db_member = member.get_id_with_both(member_id = member_id, board_id = board_id)

        if db_member is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'member not found')

        if db_member.role == members.RoleMemberEnum.HOST:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not delete your self')

        try:
            self.db.delete(db_member)
            self.db.commit()

            member_check = member.get_by_id(member_id = member_id)

            if member_check:
                return False

            return True
        except HTTPException:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'remove fail')