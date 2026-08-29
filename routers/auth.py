from fastapi import APIRouter,Depends
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import session
from starlette import status

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated=['auto'])

class CreateUserRequest(BaseModel):
    username : str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session,Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, userRequest: CreateUserRequest):
    create_user_model = Users(
        username = userRequest.username,
        mail = userRequest.email,
        first_name = userRequest.first_name,
        last_name = userRequest.last_name,
        hashed_password = bcrypt_context.hash(userRequest.password),
        role = userRequest.role,
        is_active = True
    )
    db.add(create_user_model)
    db.commit()
