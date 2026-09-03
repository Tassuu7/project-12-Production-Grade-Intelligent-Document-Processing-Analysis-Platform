"""Authentication Endpoints with Dual-Portal Session Support."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.user_service import UserService
from app.services.audit_service import AuditService
from app.api.dependencies import get_current_user, get_current_user_optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(req: UserRegister, db: Session = Depends(get_db)):
    user = UserService.create_user(db, req.email, req.username, req.full_name, req.password)
    AuditService.log_event(db, "USER_REGISTER", "USER", user_id=user.id, resource_id=str(user.id))
    return user

@router.post("/login", response_model=TokenResponse)
def login(req: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == req.username_or_email) | (User.email == req.username_or_email)
    ).first()
    
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")
        
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled.")
        
    token = create_access_token(user.id, user.role, user.email)
    refresh_token = create_refresh_token(user.id, user.role, user.email)
    
    # 1. Set general session cookie
    response.set_cookie(
        key="doc_intel_session",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=28800,
        path="/"
    )
    
    # 2. Set role-specific session cookie for seamless multi-tab dual portal support
    if user.role == "admin":
        response.set_cookie(
            key="doc_intel_admin_session",
            value=token,
            httponly=True,
            samesite="lax",
            max_age=28800,
            path="/"
        )
    else:
        response.set_cookie(
            key="doc_intel_user_session",
            value=token,
            httponly=True,
            samesite="lax",
            max_age=28800,
            path="/"
        )
    
    AuditService.log_event(db, "USER_LOGIN", "AUTH", user_id=user.id)
    
    return TokenResponse(
        access_token=token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )

@router.post("/logout")
def logout(request: Request, response: Response, user: Optional[User] = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if user:
        AuditService.log_event(db, "USER_LOGOUT", "AUTH", user_id=user.id)
        if user.role == "admin":
            response.delete_cookie(key="doc_intel_admin_session", path="/")
        else:
            response.delete_cookie(key="doc_intel_user_session", path="/")
    response.delete_cookie(key="doc_intel_session", path="/")
    return {"message": "Successfully logged out."}

@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user
