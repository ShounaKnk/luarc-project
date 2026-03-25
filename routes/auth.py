from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database.deps import get_db
from utils.deps import get_current_user
from schemas.auth import UserRegister, TokenResponse
from services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post('/register')
def register(data: UserRegister, db: Session = Depends(get_db)):
    return AuthService(db).register(data=data)

@router.post("/login", response_model=TokenResponse)
def login(
        username:str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
    ):
    return AuthService(db).login(username, password)

@router.get("/me")
def get_me(user = Depends(get_current_user)):
    return {
        "sucess": True,
        "data": {            
            "user": user
        },
        "error": None
    }