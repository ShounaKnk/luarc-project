from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import User
from utils.security import secure_password, check_password
from utils.jwt import create_acess_token
from schemas.auth import UserRegister


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        
    def register(self, data: UserRegister):
        user = User(email = data.email, password=secure_password(data.password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {
            "sucess": True,
            "data": {
                "id": user.id,
                "email": user.email 
            },
            "error": None
        }
    
    def login(self, email, password):
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user or not check_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid Credentials")
        
        token = create_acess_token({"user_id": user.id})
        
        return {"access_token": token}