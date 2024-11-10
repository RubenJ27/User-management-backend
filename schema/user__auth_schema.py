from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AuthUserCreateSchema(BaseModel):
    username: str
    email: Optional[str] = str
    full_name: Optional[str] = str
    disabled: Optional[bool] = False
    hashed_password: str


class AuthUser(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class AuthUserInDB(AuthUser):
    hashed_password: str