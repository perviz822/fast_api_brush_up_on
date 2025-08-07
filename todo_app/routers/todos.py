
from fastapi import  Depends, status, APIRouter
import models
from database import engine
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from  fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field



models.Base.metadata.create_all(bind=engine)
router= APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    


db_dependency = Annotated[Session, Depends(get_db) ]


class TodoRequest(BaseModel):
     title: str = Field(min_length=3,max_length=100)
     description: str= Field(min_length=3,max_length=100)
     priority: int =  Field(gt=0,lt=6)
     complete: bool





@router.get("/")
async def read_all( db:db_dependency ):
      return  db.query(Todos).all()
                                                      


@router.get("/todo/{todo_id}")
async def read_todo(db:db_dependency,todo_id:int):
     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
     if todo_model is not None:
          return todo_model
     raise HTTPException(status_code=404,detail="Todo not found")


@router.post("/todo")
async def create_todo(db:db_dependency,todo_request:TodoRequest):
     todo_model = Todos(**todo_request.model_dump())
     db.add(todo_model)
     db.commit()




@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,
                      todo_id:int,
                      todo_request:TodoRequest):
     todo_model = db.query(Todos).filter(Todos.id ==todo_id).first()
     if todo_model is None:
          raise HTTPException(status_code=404,detail="todo not found")
     todo_model.title = todo_request.title  # type: ignore
     todo_model.priority = todo_request.priority  # type: ignore
     todo_model.description = todo_request.description  # type: ignore
     todo_model.complete = todo_request.complete  # type: ignore
     db.commit()
     db.refresh(todo_model)
