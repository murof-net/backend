from pydantic import BaseModel, EmailStr
from datetime import date, datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # note that 0Auth2 expects 'username' instead of 'email'
    username: EmailStr | None = None

class User(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    hashed_password: str
    birthDate: date
    languages: list[str]
    registration: datetime = datetime.now()
    disabled: bool = False

class UserRegister(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    emailConfirm: EmailStr
    password: str
    passwordConfirm: str
    birthDate: date
    languages: set[str]