from fastapi import *
from fastapi.params import Body
from fastapi import APIRouter
from typing import Optional , List
from app import Models , utils
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.schemas import PostRespose
from app.schemas import PostBase , PostCreate , PostRespose

router = APIRouter()

@router.get("/posts", response_model= List[PostRespose]) #list is here to speficy that we need a list
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Models.Post).all() #this is coming as a list
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #print(posts)
    return posts

@router.post("/posts",status_code=status.HTTP_201_CREATED, response_model= PostRespose)
def createPost(post : PostCreate, db: Session = Depends(get_db)):
     #print(**post.dict())
     new_post = Models.Post(**post.dict())
     db.add(new_post)
     db.commit()
     db.refresh(new_post)
     #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title , post.content, post.publish))
     #new_post = cursor.fetchone()
     #conn.commit()
     # conveting into a dict for easy readablity
     return new_post


@router.get("/posts/{id}" , response_model= PostRespose)
async def get_post(id: int,db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts where id = %s """, str((id)))
    #post = cursor.fetchone()
    post = db.query(Models.Post).filter(Models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return post

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""DELETE FROM posts where id = %s returning * """,(str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post = db.query(Models.Post).filter(Models.Post.id == id)
    fp = post.first()

    if fp == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model= PostRespose)
async def update_post(id: int, updated_post:PostBase, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE ID =  %s RETURNING *""",
        #              (post.title, post.content, post.publish, str(id)))
    #UPDATED_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(Models.Post).filter(Models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")

    post_query.update(updated_post.dict(), synchronize_session = False)

    db.commit()

    updated_post2 = post_query.first()

    return updated_post2

