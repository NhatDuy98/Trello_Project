from sqlalchemy.orm import Session
from v1.models.users import User
from v1.schemas import user_schemas

def find_by_id(
    db: Session,
    id: int
) -> User:
    return db.query(User).filter(User.id == id).first()


def find_by_email(
    db: Session,
    email: str
) -> User:
    return db.query(User).filter(User.email == email).first()


def get_all_users_with_pagination(
        db: Session,
        page: int = 1,
        limit: int = 5,
        sort_by: str = None,
        sort_desc: bool = False,
        search: str = None,
        is_active: bool = None,
        is_delete: bool = None
) -> list[User]:
    offset = (page - 1) * limit
    query = db.query(User)

    if search:
        query = query.filter(
            (User.first_name.ilike(f"%{search}%")) |
            (User.last_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    if sort_by:
        attr = getattr(User, sort_by)
        query = query.order_by(
            attr.desc() if sort_desc else attr
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if is_delete is not None:
        query = query.filter(User.is_delete == is_delete)

    users = query.offset(offset).limit(limit).all()
    return users

def count_users(db: Session) -> int:
    return db.query(User).count()

