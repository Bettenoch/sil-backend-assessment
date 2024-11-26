from sqlmodel import Session

from app.middleware.user_auth import get_hashed_password
from app.models import User, UserCreate


def create_user(*, create_user: UserCreate, db: Session) -> User:
    hashed_password = get_hashed_password(create_user.password)

    user_obj = User.model_validate(
        create_user, update={"hashed_password": hashed_password}
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj
