from datetime import datetime, timedelta, timezone
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
from jose import jwt
router = APIRouter()

SECRET_KEY ='d79e820b57144f5468a1b63a1baff6241b62f950321ef3b0b0042206a502a33a'
ALGORITHM ='HS256'

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
    return user

def create_access_token(username:str, user_id:int, expires_delta:timedelta):
    encode = {'sub':username,'id':user_id}
    expires =datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})  #type: ignore
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)



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
    token = create_access_token(user.username, user.id, timedelta(minutes=20)) #type:ignore

    return token


