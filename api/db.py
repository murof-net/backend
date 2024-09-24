import os
from dotenv import load_dotenv
from neo4j import AsyncGraphDatabase

load_dotenv() # Load environment variables from .env file
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
if not (NEO4J_URI and NEO4J_USERNAME and NEO4J_PASSWORD):
    raise ValueError(
        "One or more .env variables are not set: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD"
        )

# Global variable for Neo4j driver
driver = None

async def init_neo4j_driver():
    """Initialize Neo4j driver during app startup."""
    global driver
    if driver is None:
        driver = AsyncGraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

async def close_neo4j_driver():
    """Close Neo4j driver during app shutdown."""
    global driver
    if driver is not None:
        await driver.close()

async def get_neo4j_session():
    """Get a Neo4j session for each request."""
    if driver is None:
        raise RuntimeError("Neo4j driver is not initialized.")
    async with driver.session() as session:
        yield session