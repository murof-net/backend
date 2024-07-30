# """
# Helper functions for endpoints.
# """

# from fastapi import Depends
# from connection import get_session

# async def execute_read_query(query, session=Depends(get_session), **params):
#     """
#     Execute a Cypher read query and return the result.
#     """
#     async def run_query(tx):
#         result = await tx.run(query, **params)
#         records = [record async for record in result]
#         return records
    
#     result = await session.execute_read(run_query)
#     return result

# async def execute_write_query(query, session=Depends(get_session), **params):
#     """
#     Execute a Cypher write query and return the result.
#     """
#     async def run_query(tx):
#         result = await tx.run(query, **params)
#         return [record async for record in result]

#     result = await session.execute_write(run_query)
#     return result