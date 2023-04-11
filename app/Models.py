from .database import Base
from sqlalchemy import Column, Integer , String, Boolean , TIMESTAMP , delete
from sqlalchemy.sql.expression import text

#this would create the SQL DB changes. Differet from schema for the datas to be required in postgres
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable=False)
    title = Column(String , nullable = False)
    content = Column(String, nullable = False)
    publised  = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))


#creating a new User model DB
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))