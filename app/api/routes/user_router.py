# app/api/routes/user_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.models.user_model import UserCreate, UserUpdate
from app.api.core.user_core import create_user_data, read_all_users, read_user_by_id, update_user_data, delete_user
from app.configurations.database import get_db
from app.configurations.security import get_current_user_id

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/readall")
def get_all(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return read_all_users(db)

@router.get("/read/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return read_user_by_id(user_id, db)

@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return create_user_data(user, db)

@router.put("/update/{user_id}")
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return update_user_data(user_id, user, db)

@router.delete("/delete/{user_id}")
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return delete_user(user_id, db)
