# backend
FastAPI / Neo4j back-end of murof.net


## Context

The `FastAPI` server is used to serve the API endpoints for the Murof application. It is responsible for handling requests from the front-end, querying the Neo4j database, and returning the appropriate responses.

Notes on technologies used:
- `async` functions for handling requests asynchronously
- `neomodel` for interacting with the Neo4j database
- `pydantic` for data validation and serialization


## Quickstart

Start **Python virtual environment** and install requirements.

```bash
python -m venv ./myenv
source menv/bin/activate
pip install -r requirements.txt
```

Start **Neo4j database** (or connect to Aura instance).

```bash
sudo systemctl start neo4j
```

Start the **FastAPI server**

```bash
fastapi dev ./api/main.py
```
