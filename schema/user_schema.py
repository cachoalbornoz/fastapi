from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    id: Optional[int] = None
    nombre: str
    email: str
    password: str
    email_verified_at: Optional[datetime] = None
    remember_token: Optional[str] = None
    ip_acceso: Optional[str] = None
    user_agent: Optional[str] = None
    ultimo_login_new: Optional[datetime] = None
    ultimo_cambio_password: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None


class UserUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    email_verified_at: Optional[datetime] = None
    remember_token: Optional[str] = None
    ip_acceso: Optional[str] = None
    user_agent: Optional[str] = None
    ultimo_login_new: Optional[datetime] = None
    ultimo_cambio_password: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None
