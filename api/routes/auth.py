from fastapi import APIRouter, HTTPException, Depends
from connection import get_session
from models.test_model import Module

from .helper import execute_read_query
from pydantic import BaseModel

router = APIRouter()

class EmailRequest(BaseModel):
    email: str

@router.post("/")
async def check_email(email_request: EmailRequest, session=Depends(get_session)):
    if email_request.email == "existing@example.com":
        return {
            "user": True,
            "email": email_request.email
            }
    else:
        return {
            "user": False,
            "email": email_request.email
            }


# @router.get("/login")

# @router.get("/register")