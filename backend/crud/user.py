from sqlalchemy.orm import Session
from db.models.user import User

def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create(db: Session, name: str, email: str, hashed_password: str) -> User:
    user = User(name = name, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
