"""
FastAPI application main file
    - Exposes API routes and data to the frontend
    - Neomodel driver for interacting with the Neo4j database
    - Makes use of async to enable asynchronous programming (i.e. concurrent requests)
        See: https://www.youtube.com/watch?v=tGD3653BrZ8 for best FastAPI async practices
"""

# MAIN : packages for connecting to the database and running the API
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# from neo4jConnection import lifespan, get_driver
from .neo4jConnection import get_driver
from fastapi.responses import FileResponse
import os

# ROUTES : API route definitions for handling endpoints
from .routes.auth.authentication import router as auth

######################################################################

app = FastAPI(
    title="Murof API", 
    # lifespan=lifespan,
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

app.include_router(auth, prefix="/auth")

######################################################################

@app.get("/")
async def root():
    """
    Root endpoint

        Endpoints are defined in the routes.py file
        and serve data to the frontend.
    """
    return {"message": "Hello World"}

@app.get("/favicon.ico")
async def favicon():
    """Load the favicon (browsers request this automatically)"""
    file_path = os.path.join(os.path.dirname(__file__), "./static/favicon.ico")
    return FileResponse(file_path)

@app.get("/test")
async def test():
    driver = await get_driver()
    async with driver.session() as session:
        # result = await session.run("RETURN 'Hello, World!' AS message")
        result = await session.run("MATCH (n) RETURN n LIMIT 1")
        record = await result.single()
    await driver.close()
    return record["n"]
