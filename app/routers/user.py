from fastapi import *
from fastapi.params import Body
from .. import Models , utils
from .. database import engine, get_db
from sqlalchemy.orm import Session
from app.schemas import userCreate , userOut

router = APIRouter()

@router.post("/users",response_model= userOut, status_code=status.HTTP_201_CREATED)
async def create_users(user:userCreate, db: Session = Depends(get_db)):

    #hash the password -user.password
    hashedpwd= utils.hash(user.password)
    user.password = hashedpwd

    createUser = Models.User(**user.dict())
    db.add(createUser)
    db.commit()
    db.refresh(createUser)
    return createUser


#path operation for geting the user
@router.get("/users/{id}", response_model= userOut)
async def get_users(id = int,db: Session = Depends(get_db)):
    user = db.query(Models.User).filter(Models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return user
