import os
# from contextlib import asynccontextmanager
from dotenv import load_dotenv
# from fastapi import FastAPI, Depends
# from neo4j import AsyncGraphDatabase, AsyncDriver
from neomodel import config

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

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """FastAPI application startup and shutdown context manager"""
#     driver = AsyncGraphDatabase.driver(
#         NEO4J_URI, 
#         auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
#         database="neo4j"
#     )
#     drivers["neo4j"] = driver
#     yield
#     await driver.close()
#     print("Driver closed")

# async def get_neo4j_driver() -> AsyncDriver:
#     """Get the Neo4j driver"""
#     return drivers["neo4j"]

# async def get_neo4j_session(driver: AsyncDriver = Depends(get_neo4j_driver)):
#     """Get a Neo4j session"""
#     async with driver.session() as session:
#         yield session