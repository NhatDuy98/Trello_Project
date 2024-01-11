from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from v1.models.members import Member
from v1.schemas import member_schemas
from v1.repository import member_repo
from v1.services import user_service, board_service
from v1.models import members

def get_all(
    db: Session,
    board_id: int,
    search: str = None
):
    db_members = member_repo.get_all(db, board_id, search)

    member_response = []

    for i in db_members:
        db_user = user_service.find_user_by_id(db, i.user_id)
        user = member_schemas.UserModel(id = i.user_id, email = db_user.email)

        member_out = member_schemas.MemberModel(id = i.id, role = i.role, user = user)

        member_response.append(member_out)

    return member_schemas.Member(data = member_response)

def add_member(
    db: Session,
    board_id: int,
    user: member_schemas.UserAdd
):
    db_member = member_repo.get_all(db, board_id, search = None)

    db_user = user_service.find_user_by_id(db, user.id)

    if db_user.email != user.email:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'email wrong')

    for i in db_member:
        if i.user_id == user.id:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'user already in group')
        
        if i.user_id == user.id and i.role == members.RoleMemberEnum.HOST:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')

    member = Member(user_id = user.id, board_id = board_id)

    db.add(member)
    db.commit()
    db.refresh(member)

    return member

def remove_member(
    db: Session,
    board_id: int,
    member_id: int
):
    db_member = member_repo.get_id_with_both(db = db, member_id = member_id, board_id = board_id)

    if db_member is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'member not found')

    if db_member.role == members.RoleMemberEnum.HOST:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not delete your self')

    db.delete(db_member)
    db.commit()

    member_check = member_repo.get_by_id(db = db, member_id = member_id)

    if member_check:
        return False

    return True
