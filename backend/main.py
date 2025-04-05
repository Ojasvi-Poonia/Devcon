from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI() #this will be used to define routes and handle requests
app.include_router(auth_router,prefix="/auth",tags=["Auth"])

@app.get("/")
def home():
    return {"message": "This is some backend"} #this is a JASON response
#this is a route decorator which tells FAstapi to execute this function when a get request is made on the / page
# if __name__ =="__main__":
#     import uvicorn #uvicorn is ASGI Async. Server Gateway Interface server that runs fastapi applications
#     uvicorn.run(app,host="127.0.0.1",port=8000,reload=True)