from pydantic import BaseModel , EmailStr
from datetime import datetime
#schema model for the body of the post.
#define response and request models.
class PostBase(BaseModel):
    title: str
    content: str
    #createtime : datetime.datetime
    publised: bool = True #setting defalut value as False , only save post. FE will give an notify to publish

class PostCreate(PostBase):
    pass #handles the same details of the postbase. kind of inheritance

class PostRespose(PostBase): #specify the data that we send back as resposne and make sure the validation is also done.
    #further simplifying the response model. Importing from the PostBase class and making the changes for the id and timestamp
    id: int
    created_at : datetime
    class Config:
        orm_mode = True

#request Model
class userCreate(BaseModel):
    email :EmailStr
    password : str
    class Config:
        orm_mode = True

#resposne model
class userOut(BaseModel):
    email: EmailStr
    id : int
    created_at: datetime
    class Config:
        orm_mode = True