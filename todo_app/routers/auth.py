from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from  models import Users
from passlib.context import CryptContext
router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')




class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str

    

@router.post("/auth")
async def create_user(createUserRequest:CreateUserRequest):
    create_user_model = Users(
        email =createUserRequest.email,
        first_name = createUserRequest.first_name,
        last_name = createUserRequest.last_name,
        is_active = True,
        hashed_password = bcrypt_context.hash(createUserRequest.password)

    )
    return{
        "user": create_user_model.hashed_password
    }




print(bcrypt_context.hash('aaasdasd'))