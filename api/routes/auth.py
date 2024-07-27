from fastapi import APIRouter, HTTPException, Depends
from connection import get_session
from models.test_model import Module

from .helper import execute_read_query
from pydantic import BaseModel

# Models for social entities: Email, Person and User
from models.socialgraph import Email, Person, User

router = APIRouter()

class EmailRequest(BaseModel):
    email: str

@router.post("/")
async def email_signup(email_request: EmailRequest, session=Depends(get_session)):
    print(email_request.email)
    """Using neomodel query"""
    modules = Email.nodes.all()

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