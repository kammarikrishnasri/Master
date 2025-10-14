# app/api/core/user_core.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.models.user_model import User, UserCreate, UserUpdate
from app.configurations.security import hash_password
from app.configurations.genarate_id import generate_prefixed_id

def read_all_users(db: Session):
    return db.query(User).all()

def read_user_by_id(user_id: str, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user_data(user_data: UserCreate, db: Session):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_id = generate_prefixed_id(db, User, "user_id", "U", 6)
    new_user = User(**{**user_data.dict(),
                       "user_id": new_id,
                       "password": hash_password(user_data.password),
                       "total_experience": user_data.total_experience or 0.0})
    try:
        db.add(new_user)
        db.flush()
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create user")

    return {"data": new_user, "status": "success", "message": f"User {new_user.full_name} created successfully"}

def update_user_data(user_id: str, data: UserUpdate, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = data.dict(exclude_unset=True)
    if "password" in update_dict:
        update_dict["password"] = hash_password(update_dict["password"])

    for key, value in update_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return {"data": user, "status": "success", "message": f"User {user_id} updated successfully"}

def delete_user(user_id: str, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}
