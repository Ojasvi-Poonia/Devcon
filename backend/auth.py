#->save user details securely 
#->validate user credentials and provide JWT tokens
#->protects routes from JWT authentications
from fastapi import HTTPException,APIRouter,Depends,status # for creating routes and handling errors
from pydantic import BaseModel
from passlib.context import CryptContext #for secure pass hashing
from datetime import datetime,timedelta # for JWT token expire timelines
from jose import JWTError,jwt # to generate and verify jwt tokens
from database import user_collection

SECRET_KEY = "hellokitty"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"] ,deprecated="auto")
# bycript pass to hash passwords before storing them so that it is safe

class UserCreate(BaseModel):
    name: str
    email:str
    password:str
class UserLogin(BaseModel):
    email:str
    password:str
class TokenData(BaseModel): #used for token validation - Ensures JWT contains a valid email
    email:str | None = None

router = APIRouter()
