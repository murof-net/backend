"""
FastAPI application main file
    - Exposes API routes and data to the frontend
    - Neomodel driver for interacting with the Neo4j database
    - Makes use of async to enable asynchronous programming (i.e. concurrent requests)
        See: https://www.youtube.com/watch?v=tGD3653BrZ8 for best FastAPI async practices
"""

# MAIN : packages for connecting to the database and running the API
from fastapi import FastAPI, Depends
from connection import lifespan, get_driver
# import asyncio # async functions e.g. asyncio.sleep(1) to avoid blocking


# ROUTES : API route definitions for handling endpoints
from routes.test_route import router as test


# MODELS : Defines node and relationship structures in the Neo4j graph DB
# from models.social_net import (
#     FriendRel, GroupMembershipRel,
#     Person, User, Group, Classroom, School
# )


# SCHEMAS : Pydantic models for request/response structure and validation/serialization
# from schemas import ModuleSchema, UserSchema


# AUTH : authentication and authorization
# from auth import jwt_handler



######################################################################

app = FastAPI(
    title="Murof API", 
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(test, prefix="/test")
# Include other routes here

# app.add_middleware(jwt_handler)



######################################################################


@app.get("/")
async def root():
    """
    Root endpoint

        Endpoints are defined in the routes.py file
        and serve data to the frontend.
    """
    return {"message": "Hello World"}



######################################################################
#  Testing authentication and authorization