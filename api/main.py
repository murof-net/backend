"""
FastAPI application main file
    - Exposes API routes and data to the frontend
    - Makes use of async to enable asynchronous programming (i.e. concurrent requests)
        See: https://www.youtube.com/watch?v=tGD3653BrZ8 for best FastAPI async practices
"""

# MAIN : packages running the API
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# ROUTES : API route definitions for handling endpoints
from .routes.auth.auth import router as auth

# DB : Neo4j connection, sessions and CRUD operations
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
    # lifespan=lifespan, # see archived db.py file
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

@app.get("/test", include_in_schema=False)
async def test():
    """Test the neo4j database connection & neomodel"""
    username = "robsyc"

    query = f"MATCH (u:User {{ username: '{username}' }}) RETURN u"
    results_adb, meta = await adb.cypher_query(query)
    user_adb = results_adb[0][0] if results_adb else None

    results_neomodel = await User.nodes.get_or_none(username=username)
    user_neomodel = {
        "hashed_password": results_neomodel.hashed_password,
        "email": results_neomodel.email,
        "username": results_neomodel.username
    } if results_neomodel else None

    return {
        "adb": user_adb if user_adb else "No records found",
        "neomodel": user_neomodel if user_neomodel else "No records found",
    }