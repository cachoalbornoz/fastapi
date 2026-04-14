from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[str] = None
    nombre: str
    email: str
    password: str
