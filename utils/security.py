from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def secure_password(password: str):
    return pwd_context.hash(password)

def check_password(input_password, hashed_password):
    return pwd_context.verify(input_password, hashed_password)