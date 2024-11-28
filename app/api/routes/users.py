import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.user_controllers import CurrentUser, SessionDep, get_current_superuser
from app.middleware.user_auth import get_hashed_password, verify_password
from app.models import (
    Message,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

router = APIRouter()


@router.get("/",dependencies=[Depends(get_current_superuser)], response_model=UsersPublic)
def get_all_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all users
    """
    statement = select(func.count()).select_from(User)

    count = session.exec(statement).one()

    user_statement = select(User).offset(skip).limit(limit)
    users = session.exec(user_statement).all()

    return UsersPublic(data=users, count=count)


@router.post("/",dependencies=[Depends(get_current_superuser)], response_model=UserPublic)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Get all users
    """
    user = crud.get_user_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.get_user_by_username(db=session, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This username is already taken please choose another one",
        )

    user = crud.create_user(db=session, create_user=user_in)
    return user


@router.post("/signup", response_model=UserPublic)
def create_account(session: SessionDep, user_in: UserRegister) -> Any:
    # Create account

    user = crud.get_user_by_email(db=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.get_user_by_username(db=session, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This username is already taken please choose another one",
        )
    user_obj = UserCreate.model_validate(user_in)
    user = crud.create_user(db=session, create_user=user_obj)
    return user


@router.patch("/my_details", response_model=UserPublic)
def update_user_details(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    user their details.
    """
    if user_in.email:
        existing_user = crud.get_user_by_email(db=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exist"
            )
    if user_in.username:
        existing_user = crud.get_user_by_username(db=session, username=user_in.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=409, detail="Username already taken")
    user_obj = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_obj)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_superuser)],
    response_model=UserPublic,
)
def update_user_privilege(
    *, session: SessionDep, user_id: uuid.UUID, user_in: UserUpdate
) -> Any:
    # Update User

    inst_user = session.get(User, user_id)
    if not inst_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist",
        )
    if user_in.email:
        existing_user = crud.get_user_by_email(db=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exist"
            )
    if user_in.username:
        existing_user = crud.get_user_by_username(db=session, username=user_in.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=409, detail="Username already taken")

    inst_user = crud.update_user(db=session, inst_user=inst_user, user_in=user_in)
    return inst_user


@router.patch("/user/password", response_model=Message)
def update_user_password(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    "Update Password"
    if not verify_password(body.initial_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.initial_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )

    hashed_password = get_hashed_password(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message="Password Updated")


@router.get("/user", response_model=UserPublic)
def get_user(current_user: CurrentUser) -> Any:
    return current_user


@router.get("/{user_id}", response_model=UserPublic)
def get_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    # Get user by their id
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesnt have enough privileges"
        )
    return user


@router.delete("/terminate_account", response_model=Message)
def delete_user(session: SessionDep, current_user: CurrentUser) -> Any:
    "Delete User Details"
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super Users Cannot delete themselves"
        )
    session.delete(current_user)
    session.commit()
    return Message(message="Cleared All User Data")


@router.delete("/{user_id}", dependencies=[Depends(get_current_superuser)])
def delete_user_privilege(
    session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
) -> Message:
    # Delete User Privilege

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )

    session.delete(user)
    session.commit()
    return Message(message="User account deleted successfully")
