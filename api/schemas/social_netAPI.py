"""
Classes for representing people in the Neo4j database using neomodel.

It provides both classes as returned by the API, and also Input classes for creating objects.

Classes:
    - PersonAPI: represents a person in the database (both dead and alive)
        - UserAPI: child of Person, represents an active user in the database
    - GroupAPI: represents a group (of users) in the database
        - ClassroomAPI: child of Group, represents a classroom in the database
        - SchoolAPI: child of Group, represents a school in the database
"""

from uuid import uuid4, UUID
from typing import Optional
from pydantic import EmailStr, Field, BaseModel
from datetime import datetime

class PersonAPI(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    firstName: str
    lastName: str
    bithDate: Optional[str] = None

class UserAPI(PersonAPI):
    username: str
    email: EmailStr
    password: str
    signUpDate: datetime
    signInDate: Optional[datetime] = None