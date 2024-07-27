"""Routes for authentication"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import neomodel
from models.social.email import Email
from connection import get_session


router = APIRouter()

class EmailRequest(BaseModel):
    email: EmailStr

@router.post("/", status_code=201)
async def signup_email(email_request: EmailRequest, session=Depends(get_session)):
    print("email_request: ", email_request)
    try: 
        email = Email.nodes.get(email=email_request.email)
        print("email already exists")
        return {
            "ok": True, 
            "message": "New signup successful or was already signed up",
            "email": email_request.email
            }
    
    except neomodel.DoesNotExist:
        email = Email(email=email_request.email).save()
        print("new email created")
        return {
            "ok": True, 
            "message": "New signup successful or was already signed up",
            "email": email_request.email
            }
    
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e


# @router.post("/login")

# @router.get("/register")