from fastapi import FastAPI, Depends, HTTPException, Path,APIRouter
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import session
from models import Todos,Users
from pydantic import BaseModel,Field
from .auth import current_user
from passlib.context import CryptContext

router = APIRouter(prefix='/user',tags=['user'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated=['auto'])

class userverify(BaseModel):
    password :str
    new_password : str = Field(min_length=6)

class userphone(BaseModel):
    new_phonenumber : str = Field(min_length=10)

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='User not authorised')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,user_verify:userverify):
    if user is None :
        raise HTTPException(status_code=401,detail="user not authorised")
    todo_model = db.query(Users).filter(Users.id==user.get('id')).first()

    if not bcrypt_context.verify(user_verify.password,todo_model.hashed_password):
        raise HTTPException(status_code=401,detail="user not authorised")
    
    todo_model.hashed_password=bcrypt_context.hash(user_verify.new_password)
    db.add(todo_model)
    db.commit()

@router.put("/phone_number",status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumbre(user:user_dependency,db:db_dependency,user_phone:userphone):
    if user is None :
        raise HTTPException(status_code=401,detail="user not authorised")
    todo_model = db.query(Users).filter(Users.id==user.get('id')).first()
    

    todo_model.Phone_number=(user_phone.new_phonenumber)
    db.add(todo_model)
    db.commit()