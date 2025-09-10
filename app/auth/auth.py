import os 
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.crud.user_crud import get_user
from app.database.database import get_db
from app.schemas.schemas import TokenData
from app.exceptions.exceptions import InvalidPasswordException, UserNotFoundException, InvalidCredentialsException


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_hashed_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email:str, password:str, db: Session):
    try:
        user = get_user(email=email, db=db)

        if not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise InvalidPasswordException(message="Invalid Password")
        
        return user
    except UserNotFoundException as e:
        raise e    

def create_access_token(data: dict,):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    jwt_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    jwt_encode = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise InvalidCredentialsException(message="Could not validate credentials")
        token_data = TokenData(email=email)
        
    except JWTError:
        raise InvalidCredentialsException(message="Could not validate credentials")
    
    user = get_user(email=token_data.email, db=db)
    return user

async def get_current_user_by_refresh_token(refresh_token: str, db: Session):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise InvalidCredentialsException(message="Could not validate credentials")
        token_data = TokenData(email=email)
        
    except JWTError:
        raise InvalidCredentialsException(message="Could not validate credentials")
    
    user = get_user(email=token_data.email, db=db)
    return user

