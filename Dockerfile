# The lab environment. No default command:
#
#   docker build -t labs .
#   docker run labs uv run python labs/session-01/trips.py
#
# The base image ships uv preinstalled.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Dependencies first: editing code below does not reinstall pandas.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# DuckDB's SQLite reader, fetched now so the labs need no network.
RUN uv run python -c "import duckdb; duckdb.sql('INSTALL sqlite')"

COPY data/ ./data/
COPY labs/ ./labs/
