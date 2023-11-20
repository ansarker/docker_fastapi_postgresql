## FastAPI, Postgresql, Docker Project

### Requirements
- Docker
- Python
- Postgresql


**Docker setup**

`docker-compose up -d`

Here, docker will install the all python dependencies along with postgresql.

**How to run application?**

Goto the root directory in terminal. and `run`

`uvicorn main:app --host 0.0.0.0 --port 8000`

or,

`python main.py`

In your web browser go to `http://localhost:8000/docs` to interact with swagger or you can use RestAPI handler like `Insomnia` or `Postman`.
