from fastapi import *
from fastapi.params import Body
app = FastAPI()
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
#import psycpog2
#from psycpog2.extras import RealDictCursor
from random import randrange
class Post(BaseModel):
    title: str
    content: str
    #createtime : datetime.datetime
    publish: bool = False  #setting defalut value as False , only save post. FE will give an notify to publish
    rating: Optional[int] = None

my_posts= [{"title":"First Post","content":"First post content","id":1},{"title":"second Post","content":"second post content","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
async def root():
    return {"message": "hello world !!sksdksdfkdsj! "}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

#@app.post("/createPost")
#def createPost(payload: dict = Body(...)):
    #print(payload)
    #p1 = payload
    #print(p1.get("title"))
    #return {"Message": "Created Post"}
#title : String
#content : string
#timeofcreate: timedate
#category :
#published or draft

@app.post("/posts")
def createPost(new_post : Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,500)
    my_posts.append(post_dict)
    #print(new_post)
    #print(new_post.dict()) # conveting into a dict for easy readablity
    return {"data": post_dict}

@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    return {"data": post}