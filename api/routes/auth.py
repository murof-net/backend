"""
Routes for authentication
 - /auth/ : Login creates a JWT token if the credentials are valid
 - /auth/register/ : Register creates a new user in the database if the credentials don't already exist
 - /auth/me/ : Get basic info on the current user
"""

from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from pydantic import BaseModel, EmailStr
from datetime import date, datetime, timedelta, timezone

import neomodel


SECRET_KEY = "6427e6b68498cb2815bd7083cd0f7cf2e9cb7d0bc3c0c8398940f10d4090fad4" # use "openssl rand -hex 32" to generate a new one
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter()


# fake_users_db = {
#     "johndoe@example.com": {
#         "firstName": "John",
#         "lastName": "Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "birthDate": "2000-01-01",
#         "languages": ["English", "French"],
#         "registration": datetime.now(),
#         "disabled": False,
#     }
# }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
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


class UserLogin(BaseModel):
    email: EmailStr
    password: str


def fake_hash_password(password: str):
    return "fakehashed" + password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


##################################################################


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password):
    return pwd_context.hash(password)


def get_user(db, email: str):
    if email in db:
        user_dict = db[email]
        return User(**user_dict)


def authenticate_user(fake_db, email: str, password: str):
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(fake_users_db, email=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


##################################################################


@router.post("/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    print(form_data.username, form_data.password)
    user = authenticate_user(fake_users_db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.email}]