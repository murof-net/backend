"""
FastAPI application main file
    - Exposes API routes and data to the frontend
    - Makes use of async to enable asynchronous programming (i.e. concurrent requests)
        See: https://www.youtube.com/watch?v=tGD3653BrZ8 for best FastAPI async practices
"""

# MAIN : packages running the API
import os
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# ROUTES : API route definitions for handling endpoints
# from .routes.auth.auth import router as auth

# DB : Neo4j connection and session handling
# from .db import lifespan, get_neo4j_session
from dotenv import load_dotenv
from neomodel import config
from neomodel import adb
from .models.social import User

load_dotenv() # Load environment variables from .env file
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
if not (NEO4J_URI and NEO4J_USERNAME and NEO4J_PASSWORD):
    raise ValueError(
        "One or more .env variables are not set: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD"
        )

drivers = {}
config.DATABASE_URL = 'neo4j+s://{}:{}@{}'.format(
    NEO4J_USERNAME, 
    NEO4J_PASSWORD, 
    NEO4J_URI.split("://")[1]
    )

######################################################################

logging.getLogger('passlib').setLevel(logging.ERROR)

app = FastAPI(
    title="Murof API", 
    # lifespan=lifespan,
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

# app.include_router(auth, prefix="/auth")

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
async def test_neo4j():
    """Test the neo4j database connection"""
    query = "MATCH (u:User {{ username: '{username}' }}) RETURN u".format(username="robsyc")
    results, meta = await adb.cypher_query(query)
    return results[0][0] if results else "No records found"

@app.get("/test_neomodel", include_in_schema=False)
async def test_neomodel():
    """Test the neomodel database connection"""
    username = "robsyc"
    result = await User.nodes.get_or_none(username=username)
    return result if result else "No records found"