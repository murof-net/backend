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
from .schemas import TokenData

######################################################################

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY") or None
ALGORITHM = os.environ.get("ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")) or 30
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS")) or 7

if not (SECRET_KEY and ALGORITHM and ACCESS_TOKEN_EXPIRE_MINUTES and REFRESH_TOKEN_EXPIRE_DAYS):
    raise ValueError(
        "One or more .env variables are not set: SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS"
        )

conf = ConnectionConfig(
    MAIL_USERNAME = "noreply@murof.net",
    MAIL_PASSWORD = "your_email_password",
    MAIL_FROM = "noreply@murof.net",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.cloudflare.com",
    MAIL_FROM_NAME = "Murof",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

######################################################################

def verify_password(plain_password, hashed_password):
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash a plain password."""
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: timedelta, token_type: str):
    """Create JWT token."""
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """Create access token."""
    return create_token(data, expires_delta, "access")

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)):
    """Create refresh token."""
    return create_token(data, expires_delta, "refresh")

######################################################################

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception

    user = await User.nodes.get_or_none(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

######################################################################

email_template_confirm = """Hi there {username},

Thank you for signing up for Murof! Please click the link below to verify your email:

{verification_link}

This link will expire in 24 hours. If you did not sign up for Murof, you can safely ignore this email.

Best,
The Murof Team
"""

email_template_warning = """Hi there {username},

We noticed that someone tried to sign up for Murof using your email address. However, this email address is already associated with an account on our platform.

What now?
- If this was not you, you can safely ignore this email.
- If this was you, please sign in using your existing account.
- If you've forgotten your password and can't sign in, reset your password: https://api.murof.net/auth/reset-password
- If you have any questions or concerns, please contact us: contact@murof.net

Best,
The Murof Team
"""

def create_verification_token(email: str):
    """Create a email verification token."""
    expiration = datetime.now() + timedelta(hours=24)
    data = {"sub": email, "exp": expiration}
    return create_token(data, timedelta(hours=24), "email_verification")

async def send_verification_email(email: EmailStr, username: str, verification_token: str):
    verification_link = f"https://api.murof.net/auth/verify/{verification_token}"
    message = MessageSchema(
        subject="Activate your Murof account",
        recipients=[email],
        body=email_template_confirm.format(email=email, username=username, verification_link=verification_link),
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_warning_email(email: EmailStr, username: str):
    message = MessageSchema(
        subject="Murof account warning",
        recipients=[email],
        body=email_template_warning.format(email=email, username=username),
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def verify_email_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return sub