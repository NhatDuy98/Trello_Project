from sqlalchemy.orm import Session
from v1.models.users import User
from v1.schemas import user_schemas

def find_by_email(
    db: Session,
    email: str
):
    return db.query(User).filter(User.email == email).first()

def create_user(
    db: Session,
    user: User
):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user