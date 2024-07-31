"""
Routes for authentication
 - /auth/ : Login creates a JWT token if the credentials are valid
 - /auth/register/ : Register creates a new user in the database if the credentials don't already exist
 - /auth/me/ : Get basic info on the current user
"""

from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status

from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from .schema import Token, User, UserRegister
from .helper import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user, authenticate_user, register_user


router = APIRouter()


@router.post("")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Login creates a JWT token if the credentials are valid
    """
    # print(form_data.username)
    user = await authenticate_user(email=form_data.username, password=form_data.password)
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
    # print(user)
    # print(user.languages)
    # print(access_token)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(form_data: UserRegister):
    """
    Register creates a new user in the database if the credentials don't already exist
    """
    # print(form_data)
    user = await register_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email address already exists",
        )
    return status.HTTP_200_OK


@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Get basic info on the current user
    """
    return current_user