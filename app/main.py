from fastapi import *
from fastapi.params import Body
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
import time

app = FastAPI()

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

@app.get("/posts/{id}")
async def get_post(id: int):
    #post = find_post(id)
    return {"data": post}