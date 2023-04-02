from fastapi import *
from fastapi.params import Body
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world !!sksdksdfkdsj! "}


@app.get("/post")
def get_post():
    return {"Data": "THis is your post"}

@app.post("/createPost")
def createPost(payload: dict = Body(...)):
    print(payload)
    p1 = payload
    print(p1.get("title"))
    return {"Message": "Created Post"}