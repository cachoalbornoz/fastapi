from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[str] 
    nombre: str
    email: str
    password: str
