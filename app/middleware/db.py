from sqlmodel import Session, create_engine, select

from app import crud
from app.middleware.preset import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    top_user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()

    if not top_user:
        user_in = UserCreate(
            name=settings.FIRST_SUPERUSER_NAME,
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )

        top_user = crud.create_user(db=session, user_create=user_in)
