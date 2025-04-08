#->save user details securely 
#->validate user credentials and provide JWT tokens
#->protects routes from JWT authentications
from fastapi import HTTPException,APIRouter,Depends,status # for creating routes and handling errors
from pydantic import BaseModel
from passlib.context import CryptContext #for secure pass hashing
from datetime import datetime,timedelta # for JWT token expire timelines
from jose import JWTError,jwt # to generate and verify jwt tokens
from database import user_collection
import os
from dotenv import load_dotenv
load_dotenv() 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))




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
def hashpass(password: str)->str:
    return pwd_context.hash(password) #it hashes a password before saving it to the data base 

def verify_password(plain_password,hashed_password)->bool:
    return pwd_context.verify(plain_password,hashed_password)# it will compare user's entered password with the hashed password 

def create_access_token(data: dict,expires_delta: timedelta = None):
    to_encode = data.copy() #copying the data to another variable so that it doesnot make changes in the original data
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15)) #utcnow=get the current utc time (Universal Coordinate Time)
    #if expires_delta is provided use that value and default time is 15 min
    to_encode.update({"exp": expire})
    #add expiration time to encode dictionary "exp " is reserved claim in the jwts which tells when the token expires
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        email: str = payload.get("sub")
        #extract sub from the decode token if sub exists returns email 
        # in JWT subs stands for subject
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
async def get_current_user(token: str):
    email = decode_access_token(token)
    user = await user_collection.find_one({"email": email})
    # await is used to wait for mongodb to return the result 
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/signup/")
async def sigup(user: UserCreate):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    hashed_password = hashpass(user.password)
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "bio": "",
        "skills": [],
        "college": "",
        "experience": "",
        "social": {
        "github": "",
        "leetcode": "",
        "linkedin": "",
        "twitter": ""
        },
        "profile_picture": ""
    }
    # user_data = {"name": user.name,"email": user.email,"password": hashed_password}
    result = await user_collection.insert_one(user_data)
    return {"message": "User registered","user_id": str(result.inserted_id)}
#checks if email is registered and if not hashes the password of the new user and adds the user 

@router.post("/login/")
async def login(user: UserLogin):
    db_user = await user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password,db_user["password"]):
        raise HTTPException(status_code=400,detail="Invalid email or password")
    token = create_access_token({"sub":db_user["email"]}, timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    return {"access_token": token, "token_type": "bearer"}
# "Bearer" means "I am giving you the token to prove who I am".
# It’s a standard way to send JWT tokens in HTTP headers.
@router.get("/me/")
async def read_user_me(user: dict = Depends(get_current_user)):
    return {"name": user["name"],"email": user["email"]}

