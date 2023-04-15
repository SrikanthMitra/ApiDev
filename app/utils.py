#has the utilites fucntions .

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") #hasing algo

def hash(password: str):
    return pwd_context.hash(password)

