"""Routes for authentication"""

from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
import neomodel
# from models.social.email import Email
# from connection import get_session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from auth import jwt_handler

router = APIRouter()

fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe@example.com",
        "fristName": "John",
        "lastName": "Doe",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice@example.com": {
        "username": "alice@example.com",
        "firstName": "Alice",
        "lastName": "Doe",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: EmailStr
    firstName: str | None = None
    lastName: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Get the user from the database by email (username according to OpenAPI spec)
    user_dict = fake_users_db.get(form_data.username)

    # If the user doesn't exist, raise an exception
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # If the password doesn't match, raise an exception
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Return JSON with an access token and a token type
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Get user, only if
    - they exists
    - was correctly authenticated
    - they are active
    """
    return current_user





# @router.post("/", status_code=201)
# async def signup_email(email_request: EmailRequest, session=Depends(get_session)):
#     print("email_request: ", email_request)
#     try: 
#         email = Email.nodes.get(email=email_request.email)
#         print("email already exists")
#         return {
#             "ok": True, 
#             "message": "New signup successful or was already signed up",
#             "email": email_request.email
#             }
    
#     except neomodel.DoesNotExist:
#         email = Email(email=email_request.email).save()
#         print("new email created")
#         return {
#             "ok": True, 
#             "message": "New signup successful or was already signed up",
#             "email": email_request.email
#             }
    
#     except Exception as e:
#         print("Error: ", e)
#         raise HTTPException(status_code=500, detail="Internal server error") from e


# @router.post("/login")

# @router.get("/register")