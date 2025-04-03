from fastapi import FastAPI
from pydantic import BaseModel
from database import add_user


app = FastAPI() #this will be used to define routes and handle requests
class User(BaseModel):
    name : str
    email : str
    skills :list[str]
@app.post("/users/")
async def create_user(user:User): #fastapi validates the incoming data is of User schema
    user_id = await add_user(user.dict()) #converts user data into dictionery and sends it to add_user
    return {"message": "User added","User id ":user_id}
@app.get("/")

def home():
    return {"message": "This is some backend"} #this is a JASON response
#this is a route decorator which tells FAstapi to execute this function when a get request is made on the / page
if __name__ =="__main__":
    import uvicorn #uvicorn is ASGI Async. Server Gateway Interface server that runs fastapi applications
    uvicorn.run(app,host="127.0.0.1",port=8000,reload=True)