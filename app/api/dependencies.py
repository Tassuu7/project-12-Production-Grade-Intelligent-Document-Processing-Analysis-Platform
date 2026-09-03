"""
FastAPI Authentication Dependencies, Multi-Portal Session Guards, and Role Access Verifiers.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.core.constants import UserRole
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user_optional(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Resolves authenticated user from Bearer header or role-specific session cookies.
    Supports simultaneous multi-tab access for User and Admin portals.
    """
    auth_token = token
    path = request.url.path

    if not auth_token:
        # Check path-specific cookies first to support simultaneous tabs
        if path.startswith("/admin"):
            auth_token = request.cookies.get("doc_intel_admin_session") or request.cookies.get("doc_intel_session")
        else:
            auth_token = request.cookies.get("doc_intel_user_session") or request.cookies.get("doc_intel_session") or request.cookies.get("doc_intel_admin_session")

    if not auth_token:
        return None

    payload = decode_token(auth_token)
    if not payload or not payload.get("sub"):
        return None

    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    return user

def get_current_user(user: Optional[User] = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in."
        )
    return user

def get_current_admin(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    auth_token = token or request.cookies.get("doc_intel_admin_session") or request.cookies.get("doc_intel_session")
    if not auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin authentication required.")
    
    payload = decode_token(auth_token)
    if not payload or not payload.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user or user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrative privileges required.")
    return user
