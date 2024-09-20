# Auth-related schemas for data validation
from pydantic import BaseModel, Field

class RegistrationForm(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, max_length=50, 
        description="The username of the user",
        example="myusername"
        )
    password: str = Field(
        ..., 
        min_length=8, 
        description="The password of the user",
        example="MyP4$$w0rd"
        )

class LoginForm(BaseModel):
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None