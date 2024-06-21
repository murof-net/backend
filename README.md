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
python3 -m venv ./myenv
source menv/bin/activate
pip install -r requirements.txt
```

Start **Neo4j database** (or connect to Aura instance).

```bash
sudo systemctl start neo4j
```
Add `.env` file with database login info

Start the **FastAPI server**

```bash
fastapi dev ./api/main.py
```

Test database connections and API endpoints at: http://127.0.0.1:8000/test/modules0