from fastapi import FastAPI
from . import models
from .database import engine
from .routers import flights, users,auth,book
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

origins = ["*"] 





app=FastAPI()             #creating a fastapi instance - "app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flights.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(book.router)



# initial path - get method 

@app.get("/")             # at endpoint "/" use GET method for the instance app and perform the below function
def root():
    return {"message": "hello y'all!!"}   # function definition 






