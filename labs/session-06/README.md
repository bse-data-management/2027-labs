# Session 6 lab — Non-relational databases and NoSQL

## Setup

From the repository root:

```bash
uv sync
docker compose up -d --build
```

This session adds MongoDB and, for part C, a PostgreSQL leader with one
follower. `--build` adds `pymongo` to the notebook image, which takes a minute the
first time. There is no new data to download.

Then open **<http://localhost:8888/lab?token=labs>** and click into
`session-06/lab.ipynb`.
