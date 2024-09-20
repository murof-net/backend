"""
FastAPI application main file
    - Exposes API routes and data to the frontend
    - Makes use of async to enable asynchronous programming (i.e. concurrent requests)
        See: https://www.youtube.com/watch?v=tGD3653BrZ8 for best FastAPI async practices
"""

# MAIN : packages for connecting to the database and running the API
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .neo4jConnection import get_neo4j_session
from fastapi.responses import FileResponse
import os

# ROUTES : API route definitions for handling endpoints
# from .routes.auth.authentication import router as auth

######################################################################

# global variables
drivers = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    from .neo4jConnection import get_neo4j_driver
    drivers["neo4j"] = await get_neo4j_driver()
    yield
    await drivers["neo4j"].close()  # Cleanup: Close driver on shutdown
    drivers.clear()

app = FastAPI(
    title="Murof API", 
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware from SvelteKit frontend at http://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:517*"],
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

        Endpoints are defined in the routes.py file
        and serve data to the frontend.
    """
    return {"message": "Welcome to the Murof API! Visit /docs for more info."}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Load the favicon (browsers request this automatically)"""
    file_path = os.path.join(os.path.dirname(__file__), "./static/favicon.ico")
    return FileResponse(file_path)

@app.get("/test")
async def test(session = Depends(get_neo4j_session)):
    result = await session.run("MATCH (n) RETURN n LIMIT 1")
    record = await result.single()
    return record["n"]
