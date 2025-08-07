from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
router = APIRouter()


@router.post("/auth")



class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str

async def create_user(createUserRequest:CreateUserRequest):

    create_user_model = Users(
        email =createUserRequest.email,
        first_name = createUserRequest.first_name,
        last_name = createUserRequest.last_name,
        is_active = True,
        hashed_password =createUserRequest.password

    )
    return{
        "user":"authenticated"
    }