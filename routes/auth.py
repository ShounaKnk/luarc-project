from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database.deps import get_db
from models.models import User
from utils.security import secure_password, check_password
from utils.jwt import create_acess_token
from utils.deps import get_current_user
from schemas.auth import UserRegister, UserLogin, TokenResponse

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post('/register')
def register(data: UserRegister, db: Session = Depends(get_db)):
    user = User(email = data.email, password=secure_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "sucess": True,
        "data": {
            "id": user.id,
            "email": user.email 
        }
    }

@router.post("/login", response_model=TokenResponse)
def login(
        username:str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
    ):
    user = db.query(User).filter(User.email == username).first()
    
    if not user or not check_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_acess_token({"user_id": user.id})
    
    return {"access_token": token}

@router.get("/me")
def get_me(user = Depends(get_current_user)):
    return {"user": user}