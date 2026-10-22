# Session 8 lab — Application programming interfaces

A small web API over the taxi database, built with FastAPI on session 7's classes.
The instructions are in `notebook.ipynb`; the code you write is in `app/`.

## Setup

From the repository root:

```bash
uv sync
docker compose up -d --build
```

This session adds FastAPI, uvicorn and httpx, already in `pyproject.toml`, put
there with `uv add fastapi uvicorn httpx`. `--build` adds them to the notebook
image and publishes port 8000 for the API.

## Running the API

The API runs in the notebook container, next to the database. In JupyterLab at
<http://localhost:8888/lab?token=labs>, open *File &rarr; New &rarr; Terminal*:

```bash
cd /app/labs/session-08
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Leave it running. The documentation is at **<http://localhost:8000/docs>**.
`--reload` restarts the server each time you save a file in `app/`; `Ctrl+C`
stops it.

## If it does not start

- *Trip in labs/session-07/models.py is not finished*: the API uses the classes
  you completed in session 7. Finish `Trip` and `Driver.trips` there first.
- *Port 8000 is in use*: `API_PORT=8001 docker compose up -d`, then use
  <http://localhost:8001/docs>. The command above stays the same.
- *relation "drivers" does not exist*: the tables are gone. Run the first cell of
  `session-07/notebook.ipynb`, which reloads them.
