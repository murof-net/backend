# backend
FastAPI / Neo4j back-end of murof.net


## Context

The [`FastAPI`](https://fastapi.tiangolo.com/tutorial/first-steps/) server is used to serve the API endpoints for the [murof](murof.net) web-application. It is responsible for handling requests from the front-end, querying the Neo4j database, and returning the appropriate responses.

Notes on technologies used:
- [`async`](https://docs.python.org/3/library/asyncio.html) functions for handling requests asynchronously
- [`neomodel`](https://neomodel.readthedocs.io/en/latest/) for interacting with the Neo4j database
- [`pydantic`](https://docs.pydantic.dev/latest/) for data validation and serialization
- authentication?!


## Quickstart

Start **Python virtual environment** and install requirements.

```bash
python3 -m venv ./myenv
source myenv/bin/activate
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

Test database connection and API endpoints at: http://127.0.0.1:8000/test/modules0

## Roadmap
- [x] root endpoint helloworld
- [x] connection with neo4j
- [x] Development bash script (also for frontend)
- [ ] JWT authentication
- [ ] first basic endpoint for sveltekit front-end request
- [ ] unit tests (with `pytest`?)
- [ ] knowledge-graph with the [Neo4j graphbuilder tool](https://llm-graph-builder.neo4jlabs.com/)
