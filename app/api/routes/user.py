# app/api/routes/user.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=Page[UserOut])
def read_users(params: Params = Depends(), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(User)
    return paginate(query, params)


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)


@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db),
                         current_user=Depends(get_current_user)):
    updated_user = crud_user.update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}", response_model=UserOut)
def delete_existing_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    deleted_user = crud_user.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
