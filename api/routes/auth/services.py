# Auth-related helper functions
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt # may want to switch to pyjwt instead
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

from ...models.social import User

from .email_templates import (
    email_confirm,
    email_warning,
    password_reset
)

######################################################################

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY") or None
ALGORITHM = os.environ.get("ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")) or 30
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS")) or 7
MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or None
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or None

if not (SECRET_KEY and ALGORITHM and ACCESS_TOKEN_EXPIRE_MINUTES and REFRESH_TOKEN_EXPIRE_DAYS and MAIL_USERNAME and MAIL_PASSWORD):
    raise ValueError(
        "One or more .env variables are not set"
        )

conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM = "no-reply@murof.net",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME = "Murof",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

######################################################################

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    return create_token(data, expires_delta, "access")

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)):
    return create_token(data, expires_delta, "refresh")

######################################################################

def create_verification_token(email: str):
    data = {"sub": email}
    return create_token(data, timedelta(hours=24), "email_verification")

async def send_verification_email(email: EmailStr, username: str, verification_token: str):
    # TODO: might want to link to frontend instead
    verification_link = f"https://murof.net/auth/register/activate?token={verification_token}"
    message = MessageSchema(
        subject="Activating your Murof account",
        recipients=[email],
        body=email_confirm.format(email=email, username=username, verification_link=verification_link),
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_warning_email(email: EmailStr, username: str):
    message = MessageSchema(
        subject="Murof account warning",
        recipients=[email],
        body=email_warning.format(email=email, username=username),
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def verify_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["type"] != token_type:
            raise HTTPException(status_code=401, detail="Invalid token")
        sub = payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return sub

def create_password_reset_token(email: EmailStr):
    data = {"sub": email}
    return create_token(data, timedelta(minutes=10), "password_reset")

def mask_email(email: EmailStr):
    email = email.split("@")
    return email[0][0] + "*"*(len(email[0])-2) + email[0][-1] + "@" + email[1]

async def send_password_reset_email(email: EmailStr, username: str, reset_token: str):
    reset_link = f"https://murof.net/auth/reset?token={reset_token}"
    message = MessageSchema(
        subject="Resetting your Murof password",
        recipients=[email],
        body=password_reset.format(email=email, username=username, reset_link=reset_link),
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(message)

######################################################################

async def get_current_user(token: str = Depends(oauth2_scheme)):
    sub = await verify_token(token, "access")
    user = await User.nodes.get_or_none(uid=sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user