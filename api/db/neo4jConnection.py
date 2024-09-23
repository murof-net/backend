"""
FastAPI Neo4j DB connection file
    - Connects to the Neo4j Aura instance
    - Creates sessions for handling CRUD operations
"""

import os
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv
from .db import get_drivers

# Environment variables
load_dotenv() # Load environment variables from .env file
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
if not (NEO4J_URI and NEO4J_USERNAME and NEO4J_PASSWORD):
    raise ValueError(
        "One or more .env variables are not set: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD"
        )

# Create an Async Neo4j driver instance
async def get_neo4j_driver():
    driver = AsyncGraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    return driver

async def get_neo4j_session():
    drivers = get_drivers()
    driver = drivers["neo4j"]  # Reuse the already initialized driver
    async with driver.session() as session:
        yield session