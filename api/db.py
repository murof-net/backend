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

async def get_neo4j_driver():
    driver = AsyncGraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    return driver

async def get_neo4j_session():
    # ideally we just want to connect to the driver once at startup and create sessions as needed
    # drivers = get_drivers() which returns the global dict of drivers
    # from .main import drivers
    driver = await get_neo4j_driver()
    async with driver.session() as session:
        yield session