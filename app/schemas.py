from pydantic import BaseModel
from datetime import datetime
#schema model for the body of the post.
class PostBase(BaseModel):
    title: str
    content: str
    #createtime : datetime.datetime
    publised: bool = True #setting defalut value as False , only save post. FE will give an notify to publish

class PostCreate(PostBase):
    pass #handles the same details of the postbase. kind of inheritance

class PostRespose(BaseModel): #specify the data that we send back as resposne and make sure the validation is also done.
    id: int
    title: str
    content: str
    publised : bool
    created_at : datetime
    class Config:
        orm_mode = True