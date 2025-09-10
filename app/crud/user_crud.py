from app.schemas.schemas import UserCreate, UserRead
from app.models.models import User
from sqlalchemy.orm import Session
from app.exceptions.exceptions import UserNotFoundException


def create_user(user: UserCreate, db:Session):
    db_user = User(username = user.username, email=user.email, hashed_password = user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(email: str, db:Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise UserNotFoundException(message="User not found")
    return user

