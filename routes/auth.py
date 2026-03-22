from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from database.deps import get_db
from models.models import User
from utils.security import secure_password, check_password
from utils.jwt import create_acess_token

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post('/register')
def register(email: str, password: str, db: session = Depends(get_db)):
    user = User(email=email, password=secure_password(password=password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user": "user created"}

@router.post("/login")
def login(email:str, password:str, db: session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not check_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    tokens = create_acess_token({"user_id": user.id})
    
    return {"access_token": token}