from typing import Any

from sqlmodel import Session, and_, select

from app.middleware.user_auth import get_hashed_password, verify_password
from app.models import User, UserCreate, UserUpdate


def create_user(*, create_user: UserCreate, db: Session) -> User:
    hashed_password = get_hashed_password(create_user.password)

    user_obj = User.model_validate(
        create_user, update={"hashed_password": hashed_password}
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def update_user(*, db: Session, inst_user: User, user_in: UserUpdate) -> Any:
    user_obj = user_in.model_dump(exclude_unset=True)
    auth_data = {}
    if "password" in user_obj:
        password = user_obj["password"]
        hash_password = get_hashed_password(password)
        auth_data["hashed_password"] = hash_password

    inst_user.sqlmodel_update(user_obj, update=auth_data)
    db.add(inst_user)
    db.commit()
    db.refresh(inst_user)
    return inst_user


def get_user_by_username(*, db: Session, username: str, email: str) -> User | None:
    statement = select(User).where(and_(User.username == username, User.email == email))
    inst_user = db.exec(statement).first()
    if not inst_user:
        return None
    return inst_user


def get_user_by_email(*, db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    inst_user = db.exec(statement).first()
    return inst_user


def authenticate_by_password(*, db: Session, email: str, password: str) -> User | None:
    inst_user = get_user_by_email(db=db, email=email)
    if not inst_user:
        return None
    if not verify_password(password, inst_user.hashed_password):
        return None
    return inst_user
