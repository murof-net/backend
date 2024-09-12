from typing import Annotated
from fastapi import HTTPException, status, Depends

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from .schema import Token, TokenData, User, UserRegister

from datetime import timedelta, datetime, timezone

from ...models.social import User as UserModel, Language as LanguageModel

import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the plain text password matches the hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    """
    Hash the plain text password
    """
    return pwd_context.hash(password)


async def get_user(email: str) -> UserModel | None:
    """
    Get the user with the given email from the database
    """
    return UserModel.nodes.get_or_none(email=email)


async def authenticate_user(email: str, password: str):
    """
    Authenticate the user with the given email and password
    """
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create an access token with the given data and expiration time
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Get the current user from the token
    """
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
    user = await get_user(email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the current active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User has not been activated")
    return current_user


async def register_user(form: UserRegister):
    """
    Register a new user
    """
    # Check if user with the same email already exists
    existing_user = await get_user(email=form.email)
    if existing_user:
        return False
    # Create new user
    hashed_password = get_hashed_password(form.password)
    user = UserModel(
        first_name=form.firstName,
        last_name=form.lastName,
        email=form.email,
        hashed_password=hashed_password,
        birth_date=form.birthDate,
        registration=datetime.now(),
        is_active=True
    ).save()
    # Create languages and connect
    for language in form.languages:
        lang = LanguageModel(name=language).save()
        user.languages.connect(lang)
    return True
