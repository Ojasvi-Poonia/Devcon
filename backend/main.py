from fastapi import FastAPI
from auth import router as auth_router
from user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv() 

app = FastAPI(title="devcon app") #this will be used to define routes and handle requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #for devleopment add frontend domain here\
    allow_credentials = True,#allow cookies and credentials like JWT we are using here
    allow_methods=["*"],#allow GET,PUT,POST methods we can also restrict as allow_methods=["GET","POST"]
    allow_headers=["*"],
)
app.include_router(auth_router,prefix="/auth",tags=["Auth"])
app.include_router(user_router,prefix="/user",tags=["User"])

@app.get("/")
def home():
    return {"message": "welcome to devcon app", "status": "running"} #this is a JASON response
#this is a route decorator which tells FAstapi to execute this function when a get request is made on the / page
if __name__ =="__main__":
    import uvicorn #uvicorn is ASGI Async. Server Gateway Interface server that runs fastapi applications
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)