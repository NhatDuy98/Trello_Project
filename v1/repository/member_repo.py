from sqlalchemy.orm import Session
from v1.models.members import Member
from v1.models.users import User

async def add_member(
    db: Session,
    member: Member
) -> Member:
    db.add(member)
    db.commit()
    db.refresh(member)

def get_all(
    db: Session,
    board_id: int,
    search: str = None
):

    members = db.query(Member).outerjoin(User, Member.user_id == User.id).filter(Member.board_id == board_id)

    if search:
        members = members.filter((User.email.ilike(f'%{search}%')))


    return members.all()

def get_by_id(
    db: Session,
    member_id: int
):
    return db.query(Member).filter(Member.id == member_id).first()

def get_id_with_both(
    db: Session,
    board_id: int,
    member_id: int
):
    return db.query(Member).filter(Member.board_id == board_id and Member.id == member_id).first()