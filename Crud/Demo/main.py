from fastapi import FastAPI,Depends,status,HTTPException
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app=FastAPI()
 
class PostBase(BaseModel):
    title:str
    content:str
    user_id:int
class UserBase(BaseModel):
    username:str 

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]  
     
@app.post("/post/",status_code=status.HTTP_201_CREATED)
async def create_post(post:PostBase,db:db_dependency):
    db_post=models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.get("/post/{post_id}",status_code=status.HTTP_200_OK)
async def get_post(post_id:int,db:db_dependency):
    post=db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail='post not found')
    return post

@app.delete("/post/{post_id}",status_code=status.HTTP_200_OK)
async def delete_post(post_id:int,db:db_dependency):
    post=db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post not found ')
    db.delete(post)
    db.commit()

@app.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase,db:db_dependency):
    db_user=models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()  # Add parentheses to call the method
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')
    return user 

  
      

