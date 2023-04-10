from pydantic import BaseModel

#schema model for the body of the post.
class Post(BaseModel):
    title: str
    content: str
    #createtime : datetime.datetime
    publised: bool  #setting defalut value as False , only save post. FE will give an notify to publish

