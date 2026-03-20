from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.deps import get_db
from models.models import User

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/")
def test_api():
    return ("test working")

class Item(BaseModel):
    name: str
    price: int

items = []

@router.post("/item")
def create_item(item: Item):
    items.append(item)
    return {
        "name": item.name,
        "price": item.price,
        "status": "created"
    }

@router.get("/list_items")
def list_items():
    return items

@router.get("/item/{item_name}")
def search_item(item_name: str):
    found_item = [item for item in items if item.name == item_name ]
    if found_item:
        return found_item
    return {"message": "not found"}


@router.post("/create-user")
def create_user(email: str, password:str, db:Session = Depends(get_db)):
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user