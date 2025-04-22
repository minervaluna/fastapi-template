# app/api/routes/token.py
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.jwt_handler import create_access_token
from app.core.security import verify_password
from app.crud.user import get_user_by_username

router = APIRouter(prefix="/token", tags=["users"])


@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not found: {form_data.username}",
        )
    print(f"hashed_password: {user.hashed_password}")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Passwords do not match",
        )
    access_token = create_access_token(data={
        "id": user.id,
        "username": user.username
    })
    return {"access_token": f"Bearer {access_token}", "token_type": "bearer"}
