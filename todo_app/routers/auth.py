from fastapi import FastAPI
from fastapi import APIRouter
router = APIRouter()
app=FastAPI()


@router.get("/auth")

async def get_user():
    return{
        "user":"authenticated"
    }