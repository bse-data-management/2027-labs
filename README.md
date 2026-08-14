# Data Management (23D021) — labs

Lab code for Data Management, MSc in Data Science, Barcelona School of
Economics.

```
labs/session-NN/     one folder per session, each with its own README
data/                shared datasets (downloaded ones are not committed)
scripts/             shared: downloads and prepares the datasets
Dockerfile           the lab environment
docker-compose.yml   the services the labs run on
pyproject.toml       dependencies, and all three quality tools in one file
```

## Setup

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/),
[uv](https://docs.astral.sh/uv/getting-started/installation/) and
[VS Code](https://code.visualstudio.com/) with the Python and Jupyter
extensions, then clone this repository.

Each lab starts from its own README under `labs/`.

## Notebooks

`docker compose up -d` serves JupyterLab from the lab environment. Two ways in:

- **Browser** — <http://localhost:8888/lab?token=labs>
- **VS Code** — open the notebook, then **Select Kernel** &rarr; *Existing Jupyter
  Server…* &rarr; `http://localhost:8888/?token=labs`

Either way the code runs in the container, and what you type is saved to your own
`labs/` folder.

## Checks

From the repository root:

```bash
uv sync
uv run pytest
uv run ruff format . && uv run ruff check .
uv run pyright
```

On a clean clone, all pass.