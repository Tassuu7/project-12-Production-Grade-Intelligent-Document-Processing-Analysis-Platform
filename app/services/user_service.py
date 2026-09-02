"""User Management Business Service."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.exceptions import ValidationException

class UserService:
    @staticmethod
    def create_user(db: Session, email: str, username: str, full_name: str, password: str, role: str = "user") -> User:
        if db.query(User).filter(User.email == email).first():
            raise ValidationException("Email address already registered.")
        if db.query(User).filter(User.username == username).first():
            raise ValidationException("Username already in use.")
            
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
