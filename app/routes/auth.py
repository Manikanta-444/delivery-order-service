from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hash import get_password_hash, verify_password
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_create.username, User.email == user_create.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")
    user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
        role=user_create.role.value
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User registered", "username": user.username, "email": user.email, "role": user.role}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    print(f"query: {db.query(User).filter(User.email == form_data.username)}")
    print(f"form_data.username: {form_data.username}")
    print(f"form_data.password: {form_data.password}")
    print(f"user: {user}")
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
