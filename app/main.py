from fastapi import *
from fastapi.params import Body
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
import time
from . import Models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
Models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    #createtime : datetime.datetime
    publish: bool = False  #setting defalut value as False , only save post. FE will give an notify to publish
    rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(host='localhost',database = 'fastapi', user= 'postgres', password = 'password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Dataase connection sucessfull")
        break
    except Exception as error:
        print("connectiing to DB Failed")
        print("Error ",error)
        time.sleep(2)
#my_posts= [{"title":"First Post","content":"First post content","id":1},{"title":"second Post","content":"second post content","id":2}]

@app.get("/")
async def root():
    return {"message": "hello world !!sksdksdfkdsj! "}

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    return {"status":"Sucess "}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def createPost(post : Post):
     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title , post.content, post.publish))
     new_post = cursor.fetchone()
     conn.commit()
     # conveting into a dict for easy readablity
     return {"data": new_post}


@app.get("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts where id = %s """, str((id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return {"data": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id = %s returning * """,(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE ID =  %s RETURNING *""",
                   (post.title, post.content, post.publish, str(id)))
    UPDATED_post = cursor.fetchone()
    conn.commit()

    if UPDATED_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return {"data": UPDATED_post}