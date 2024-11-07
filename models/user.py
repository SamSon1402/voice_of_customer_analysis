from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    USER = "user"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserPermission(str, Enum):
    READ_METRICS = "read:metrics"
    WRITE_METRICS = "write:metrics"
    MANAGE_ALERTS = "manage:alerts"
    MANAGE_USERS = "manage:users"
    ADMIN_ALL = "admin:all"

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
    permissions: List[UserPermission] = []

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    permissions: Optional[List[UserPermission]] = None
    password: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            if not any(c.isupper() for c in v):
                raise ValueError('Password must contain at least one uppercase letter')
            if not any(c.islower() for c in v):
                raise ValueError('Password must contain at least one lowercase letter')
            if not any(c.isdigit() for c in v):
                raise ValueError('Password must contain at least one number')
        return v

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    settings: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: Optional[str]
    role: UserRole
    status: UserStatus
    permissions: List[UserPermission]
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserSession(BaseModel):
    user_id: str
    session_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class UserActivityLog(BaseModel):
    id: str
    user_id: str
    action: str
    details: Dict[str, Any]
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class UserPreferences(BaseModel):
    theme: Optional[str] = "light"
    notifications_enabled: bool = True
    email_notifications: bool = True
    timezone: str = "UTC"
    language: str = "en"
    dashboard_layout: Dict[str, Any] = {}