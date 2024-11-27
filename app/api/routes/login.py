# app/api/routes/login.py
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.user_controllers import CurrentUser, SessionDep
from app.middleware import user_auth
from app.middleware.preset import settings
from app.models import Token, UserPublic

router = APIRouter()


@router.post("/login/authenticated_token")
def user_login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    get access token
    """
    user = crud.authenticate_by_password(
        db=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=user_auth.create_token_access(user.id, expires_delta=token_expiry)
    )


@router.post("/login/test-access-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
