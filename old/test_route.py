# """
# Test route for testing
# """

# from fastapi import APIRouter, Depends
# from connection import get_session
# from models.test_model import Module

# from .helper import execute_read_query


# router = APIRouter()


# @router.get("/modules0")
# async def get_modules0(limit: int = 10, session = Depends(get_session)):
#     """Using run(Cypher query)"""
#     query = "MATCH (m:Module) RETURN m LIMIT $limit"
#     result = await session.run(query, limit=limit)
#     modules = [record["m"] for record in await result.data()]
#     return modules


# @router.get("/modules1")
# async def get_modules1(limit: int = 10, session = Depends(get_session)):
#     """Using explicit read query function"""
#     query = "MATCH (m:Module) RETURN m LIMIT $limit"
#     result = await execute_read_query(query, session, limit=limit)
#     modules = [record["m"] for record in result]
#     return modules


# @router.get("/modules2")
# async def get_group(limit: int = 10):
#     """Using neomodel query"""
#     modules = Module.nodes.all()[:limit]
#     return modules