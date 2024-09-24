"""
FastAPI application main file
    - Exposes API routes and data to the frontend
    - Makes use of async to enable asynchronous programming (i.e. concurrent requests)
        See: https://www.youtube.com/watch?v=tGD3653BrZ8 for best FastAPI async practices
"""

# MAIN : packages running the API
import os
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# DB : Neo4j connection and session handling
from .db import lifespan, get_neo4j_session
from .models.social import User

# ROUTES : API route definitions for handling endpoints
from .routes.auth.auth import router as auth

######################################################################

logging.getLogger('passlib').setLevel(logging.ERROR)

app = FastAPI(
    title="Murof API", 
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware from SvelteKit frontend
origins = [
    "http://localhost:517*",
    "https://murof.net"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(auth, prefix="/auth")

######################################################################

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"message": "Welcome to the Murof API! Visit /docs for more info."}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Load the favicon (browsers request this automatically)"""
    file_path = os.path.join(os.path.dirname(__file__), "./static/favicon.ico")
    return FileResponse(file_path)

######################################################################

@app.get("/test_neo4j", include_in_schema=False)
async def test_neo4j(session = Depends(get_neo4j_session)):
    """Test the neo4j database connection"""
    username = "robsyc"
    result = await session.run(
        "MATCH (u:User {username: $username}) RETURN u", 
        username=username
    )
    record = await result.single()
    return record["u"] if record else "No records found"

@app.get("/test_neomodel", include_in_schema=False)
async def test_neomodel(session = Depends(get_neo4j_session)):
    """Test the neomodel database connection"""
    username = "robsyc"
    result = User.nodes.get_or_none(username=username)
    return result if result else "No records found"