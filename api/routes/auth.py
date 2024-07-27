"""Routes for authentication"""

from fastapi import APIRouter, HTTPException, Depends
from connection import get_session

# from .helper import execute_read_query

# Pydantic validation tools
from pydantic import BaseModel
from pydantic.networks import EmailStr

# Neo4j models
from models.social.email import Email

################################################################

router = APIRouter()

class EmailRequest(BaseModel):
    email: EmailStr

@router.post("/")
async def signup_email(email_request: EmailRequest, session=Depends(get_session)):
    print(email_request.email)
    if email_request.email == "existing@example.com":
        return {
            "ok": True,
            "email": email_request.email
            }
    else:
        return {
            "ok": False,
            "email": email_request.email
            }


# @router.get("/login")

# @router.get("/register")