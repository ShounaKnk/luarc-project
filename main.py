from fastapi import FastAPI
from routes import test
from database.database import Base, engine
from models import models

app = FastAPI()

app.include_router(test.router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return("its working")