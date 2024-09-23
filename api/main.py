"""
FastAPI application main file
    - Exposes API routes and data to the frontend
    - Makes use of async to enable asynchronous programming (i.e. concurrent requests)
        See: https://www.youtube.com/watch?v=tGD3653BrZ8 for best FastAPI async practices
"""

# MAIN : packages for connecting to the database and running the API
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
# from .db.db import get_drivers
# from .db.neo4jConnection import get_neo4j_session
import logging

# ROUTES : API route definitions for handling endpoints
from .routes.auth.auth import router as auth

######################################################################

logging.getLogger('passlib').setLevel(logging.ERROR)

######################################################################
# TEMPORARY CHECK TO SEE HOW VERCEL HANDLES THIS
import os
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
if not (NEO4J_URI and NEO4J_USERNAME and NEO4J_PASSWORD):
    raise ValueError(
        "One or more .env variables are not set: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD"
        )

drivers = {}

# Create an Async Neo4j driver instance
async def get_neo4j_driver():
    driver = AsyncGraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    return driver

async def get_neo4j_session():
    driver = await get_neo4j_driver()
    async with driver.session() as session:
        yield session

######################################################################

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # from .db.neo4jConnection import get_neo4j_driver
#     drivers["neo4j"] = await get_neo4j_driver()
#     yield
#     await drivers["neo4j"].close()  # Cleanup: Close driver on shutdown
#     drivers.clear()

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

@app.get("/test", include_in_schema=False)
async def test_db(session = Depends(get_neo4j_session)):
    """Test the database connection"""
    result = await session.run("MATCH (n) RETURN n LIMIT 1")
    record = await result.single()
    return record["n"] if record else "No records found"
