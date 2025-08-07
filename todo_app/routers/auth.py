from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from  models import Users
from typing import Annotated
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    


db_dependency = Annotated[Session, Depends(get_db) ]

    
def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return    
    if  not bcrypt_context.verify(password,user.hashed_password):
        return False
    return True 



@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(
    db:db_dependency,
    createUserRequest:CreateUserRequest):

    create_user_model = Users(
        username=createUserRequest.username,
        email =createUserRequest.email,
        first_name = createUserRequest.first_name,
        last_name = createUserRequest.last_name,
        is_active = True,
        hashed_password = bcrypt_context.hash(createUserRequest.password)

    )

    db.add(create_user_model)
    db.commit()
 

@router.post("/token")
async def  login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                  db:db_dependency):
    

    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        return "Failed authentication"
    
    return 'Authentication succesfull'


