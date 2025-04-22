# app/api/deps.py
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.jwt_handler import decode_access_token
from app.crud import user as crud_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)):
    # token 格式："Bearer <token>"
    if token.startswith("Bearer "):
        token = token[7:]
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    user_id = payload.get("id")
    print(f"user_id: {user_id}")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    db_user = crud_user.get_user(db, int(user_id))
    print(f"user: {db_user}")
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return db_user
