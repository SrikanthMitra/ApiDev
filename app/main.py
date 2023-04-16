from fastapi import *
from fastapi.params import Body
from datetime import datetime
from typing import Optional , List
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
import time
from . import Models , utils
from .database import engine, get_db
from sqlalchemy.orm import Session
Models.Base.metadata.create_all(bind=engine)
from .schemas import PostBase , PostCreate , PostRespose , userCreate , userOut
from .routers import post, user

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") #hasing algo

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database = 'fastapi', user= 'postgres', password = 'password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection sucessfull")
        break
    except Exception as error:
        print("Connection to DB Failed, Check the error  ")
        print("Error ",error)
        time.sleep(2)
#my_posts= [{"title":"First Post","content":"First post content","id":1},{"title":"second Post","content":"second post content","id":2}]


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "hello world !!sksdksdfkdsj! "}

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    posts = db.query(Models.Post).all()
    print(posts)
    return posts


#User Module Level Operations



