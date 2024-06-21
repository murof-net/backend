"""
FastAPI Neo4j DB connection file
    - Connects to the Neo4j DB through neomodel
    - Creates sessions for handling CRUD operations
"""

from contextlib import asynccontextmanager
from fastapi import Depends
from neo4j import AsyncGraphDatabase, AsyncDriver
from neomodel import config
from dotenv import load_dotenv
import os


# Environment variables
load_dotenv() # Load environment variables from .env file
NEO4J_URI = os.getenv("NEO4J_URI", default = "neo4j://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", default = "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", default = "password")
if not (NEO4J_URI and NEO4J_USERNAME and NEO4J_PASSWORD):
    raise ValueError(
        "One or more .env variables are not set: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD"
        )

# Set up the Neo4j driver
shared_context = {}
config.DATABASE_URL = "bolt://" + NEO4J_USERNAME + ":" + NEO4J_PASSWORD + "@" + NEO4J_URI.split("://")[1]
config.DATABASE_NAME = "neo4j"

@asynccontextmanager
async def lifespan(app):
    """
    Lifespan function for FastAPI to manage the Neo4j driver
        - Driver is created and closed when the lifespan ends
        - The driver is shared between all endpoints (like a global variable)
    """
    driver = AsyncGraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        database="neo4j"
    )
    shared_context["driver"] = driver
    yield
    await driver.close()
    print("Driver closed")

async def get_driver() -> AsyncDriver:
    """
    Dependency function to get the shared Neo4j driver
    """
    return shared_context["driver"]

async def get_session(driver: AsyncDriver = Depends(get_driver)):
    """
    Dependency function to get a Neo4j session
    """
    async with driver.session() as session:
        yield session
