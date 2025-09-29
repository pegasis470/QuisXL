from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from models import User
from schemas import UserCreate, Login,validateLogin
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from utils import genrate_auth_token

load_dotenv()
AUTH_KEY=os.getenv("AUTH_KEY_GEN",None)
# Create the FastAPI router
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username/email/phone already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email_id == user.email_id).first():
        raise HTTPException(status_code=400, detail={"error":"Email already exists","username":str(db.query(User).filter(User.email_id == user.email_id).first().username)})
    if db.query(User).filter(User.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail={"error":"Phone number already exists","username":str(db.query(User).filter(User.phone_number == user.phone_number).first().username)})
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        name=user.name,
        phone_number=user.phone_number,
        email_id=user.email_id,
        organization=user.organization,
        username=user.username,
        password_hash=hashed_password,
        auth_token = genrate_auth_token(AUTH_KEY),
        status = "Offline"
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.user_id}


@router.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    print(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if db_user.status == "Online":
        raise HTTPException(status_code=400, detail="User already logged in")
    db_user.auth_token = genrate_auth_token(AUTH_KEY)
    db_user.status = "Online"
    db.commit()
    return {"message": "Login successful", "user_id": db_user.user_id, "status": db_user.status , "auth_token": db_user.auth_token, "statusCode":200}
 
@router.post("/logout/{user_id}")
def logout(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.auth_token = "NO AUTH"
    user.status = "Offline"
    db.commit()
    
    return {"message": "User logged out", "status": user.status}

@router.post("/validate-token")
def validate_auth_token(user:validateLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user.user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.auth_token == "NO AUTH":
        return {"valid": False}
    if user.status == "Offline":
        return {"valid": False}
    if user.auth_token != user.auth_token:
        return {"valid": False}
    return {"valid": True, "auth_token": user.auth_token}