# Auth-related schemas for data validation
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class RegistrationForm(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, max_length=32, 
        description="The username of the user",
        example="myusername"
        )
    email: EmailStr = Field(
        ..., 
        description="The email of the user",
        example="email@example.com"
        )
    password: str = Field(
        ..., 
        min_length=8, max_length=32,
        description="The password of the user",
        example="Pa$$w0rd"
        )
    
    # validators: return 422 error + msg if validation fails
    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not re.match(r"^[a-zA-Z0-9_]*$", value):
            raise ValueError("Username can only contain letters, numbers and underscores")
        return value
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!?@#$%^&*]", value):
            raise ValueError("Password must contain at least one special character")
        return value

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None