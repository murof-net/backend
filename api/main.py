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
from .db import get_neo4j_session

# ROUTES : API route definitions for handling endpoints
from .routes.auth.auth import router as auth


######################################################################

# drivers = {}  # global drivers dict to store Neo4j driver (better practice)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI application startup and shutdown context manager"""
    print("Application is starting up!")
    yield
    print("Application is shutting down!")

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

@app.get("/test", include_in_schema=False)
async def test_db(session = Depends(get_neo4j_session)):
    """Test the database connection"""
    result = await session.run("MATCH (n) RETURN n LIMIT 1")
    record = await result.single()
    return record["n"] if record else "No records found"
