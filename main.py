#we came in
from fastapi import FastAPI
from routes import test, auth, coupons
from database.database import Base, engine

app = FastAPI()

app.include_router(test.router)
app.include_router(auth.router)
app.include_router(coupons.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return("its working")