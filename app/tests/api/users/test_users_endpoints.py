#app/tests/api/users/test_users_endpoints.py
from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.middleware.preset import settings
from app.models import UserCreate

faker = Faker()



def test_get_public_user(
    client: TestClient, users_token_header: dict[str, str]
)-> None:
    req = client.get(f"{settings.API_V1_STR}/users/user", headers=users_token_header)
    current_user = req.json()
    assert current_user

def test_get_current_superuser (
    client: TestClient, superuser_token:dict[str, str]
) -> None:
    req = client.get(f"{settings.API_V1_STR}/users/user", headers=superuser_token)
    assert 200 <= req.status_code < 300
    current_super_user = req.json()
    
    assert current_super_user
    
    
def test_create_new_user(
    client:TestClient, superuser_token:dict[str, str], db: Session
)-> None:
    email= faker.email()
    name= faker.name()
    username = faker.user_name()
    password=faker.password()
    
    user_obj = {
        "email":email,
        "name":name,
        "username":username,
        "password": password
    }
    req = client.post(
        f"/sil/api/users/", headers=superuser_token, json=user_obj
    )
    
    created_user = req.json()
    assert created_user
    
    # user = crud.get_user_by_username(db=db, username=username)
    # user = crud.get_user_by_email(db=db, email=email)
    

def test_should_return_existing_user(
    client: TestClient, superuser_token: dict[str, str], db: Session
) -> None:
    email= faker.email()
    name= faker.name()
    username = faker.user_name()
    password=faker.password()
    
    user_in = UserCreate(email=email, username=username, name=name, password=password)
    
    user = crud.create_user(create_user=user_in, db=db)
    user_id = user.id
    
    req = client.get(
        f"/sil/api/users/{user_id}", headers=superuser_token
    )
    
    # assert 200 <= req.status_code < 300
    inst_user = req.json()
    