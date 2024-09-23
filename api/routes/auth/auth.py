import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import RegistrationForm, Token
from ...db.neo4jConnection import get_neo4j_session
from .services import get_password_hash, verify_password, create_access_token, create_refresh_token, get_current_user
from jose import JWTError, jwt


router = APIRouter(tags=["auth"])
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(form: RegistrationForm, session = Depends(get_neo4j_session)):
    """Register endpoint, validates form and creates a new user"""
    # Check if username is already taken
    result = await session.run(
        "MATCH (u:User) WHERE u.username = $username RETURN u",
        username=form.username, email=form.email
    )
    if await result.single():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if email is already taken (without letting the client know)
    # TODO: Implement email uniqueness check & send email verification

    # Create user
    hashed_password = get_password_hash(form.password)
    await session.run(
        "CREATE (u:User {username: $username, email: $email, hashed_password: $password})",
        username=form.username, email=form.email, password=hashed_password
    )
    return {"message": "User registration successful"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends(), session=Depends(get_neo4j_session)):
    """Login endpoint, validates form, authenticates user and creates JWT tokens"""
    is_email = "@" in form.username
    if is_email:
        query = "MATCH (u:User {email: $identifier}) RETURN u"
    else:
        query = "MATCH (u:User {username: $identifier}) RETURN u"

    result = await session.run(query, identifier=form.username)
    user = await result.single()

    if user is None or not verify_password(form.password, user['u']['hashed_password']):
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
            )
    data = {
        "username": user['u']['username'],
        "email": user['u']['email']
    }
    return {
        "access_token": create_access_token(data=data), 
        "refresh_token": create_refresh_token(data=data),
        "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str):
    """Refresh access token endpoint"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {
        "access_token": create_access_token(data={"sub": username}),
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user['username'],
        "email": current_user['email']
    }