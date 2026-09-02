"""User authentication and profile request/response schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    storage_used_bytes: int
    document_count: int
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)

class UserAdminCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str
    password: str = Field(..., min_length=8)
    role: str = "user"
    is_active: bool = True

class UserAdminUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
