from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Annotated

class RegisterRequest(BaseModel):
    email: Annotated[EmailStr, Field(..., description="User's email address")]
    password: Annotated[str, Field(..., description="User's password")]
    role: Annotated[str, Field(..., description="User's role", examples=["user"])]

class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(..., description="User's email address")]
    password: Annotated[str, Field(..., description="User's password")]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class Google_URL(BaseModel):
    google_auth_url: str
class LoginResponse(BaseModel):
    access_token: str