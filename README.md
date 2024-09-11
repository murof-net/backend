# backend
FastAPI / Neo4j back-end of murof.net


## Context

The [`FastAPI`](https://fastapi.tiangolo.com/tutorial/first-steps/) server is used to serve the API endpoints for the [murof](murof.net) web-application. It is responsible for handling requests from the front-end, querying the Neo4j database, and returning the appropriate responses.

Notes on technologies used:
- [`async`](https://docs.python.org/3/library/asyncio.html) functions for handling requests asynchronously
- [`neomodel`](https://neomodel.readthedocs.io/en/latest/) for interacting with the Neo4j database
- [`pydantic`](https://docs.pydantic.dev/latest/) for data validation and serialization
- [`jwt`](https://jwt.io/), [`bcrypt`](https://github.com/pyca/bcrypt/) and [`passlib`](https://passlib.readthedocs.io/en/stable/) for authentication


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

Check out the autamatic `/docs` route

## Roadmap
- [x] root endpoint helloworld
- [x] connection with neo4j
- [x] Development bash script (also for frontend)
- [x] JWT authentication
- [ ] Host on Vercel serverless
- [ ] Proper JWT auth with SvelteKit frontend (or without in case API is used stand-alone)
- [ ] update startup to use neo4j desktop DBMS instead of systemctl
- [ ] first basic endpoint for sveltekit front-end request
- [ ] unit tests (with `pytest`?)
- [ ] api setup and documentation
- [ ] knowledge-graph with the [Neo4j graphbuilder tool](https://llm-graph-builder.neo4jlabs.com/) or more intricate custom LangChain setup + Google Gemini (flash)
