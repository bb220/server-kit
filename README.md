# server-kit

Starter for modern python server projects.

### Tech Stack
| Description | Name |
| --- | --- |
| Web framework and server | [FastAPI](https://fastapi.tiangolo.com/) (+ [Uvicorn](https://www.uvicorn.org/))|
| Config loading | [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| Test framework | [Pytest](https://docs.pytest.org/) |
| Linting and formatting tool | [Ruff](https://docs.astral.sh/ruff/) |
| Dependency management and task runner | [uv](https://docs.astral.sh/uv/) |

## TODO
- [x] init project with `uv`
- [x] scaffold FastAPI app, async route handlers
- [x] configure ruff for linting/formatting checks
- [x] set up test suite
- [x] CI/CD github workflow
- [x] config loading
- [x] set up logging
- [ ] ORM + lite DB + migrations
- [ ] async for I/O operations
- [ ] integrate 3rd-party service

## Quickstart
```bash
uv sync
docker compose up -d postgres
uv run fastapi dev src/server_kit/main.py
```

The local Postgres service in `compose.yml` uses the same defaults as `.env.example`:
- host: `localhost`
- port: `5432`
- database: `server_kit`
- user: `postgres`
- password: `postgres`

## Logging
- App logs use `structlog`
- `LOG_FORMAT=dev` renders readable local logs
- `LOG_FORMAT=json` renders production-style JSON for app and stdlib loggers, including `uvicorn`
- Each request gets an `X-Request-ID` that is bound into the log context

## Linter and Formatter
```bash
uv run ruff check
uv run ruff format
```

## Tests
```bash
uv run pytest
uv run pytest -m integration
```

## Configuration
- Config is loaded from the env
- Local config can be loaded from `.env`
  - Copy `.env.example` and adjust values.
- Database-related config is also loaded from `.env`
  - `DATABASE_URL`
  - `DATABASE_POOL_SIZE`
  - `DATABASE_MAX_OVERFLOW`
  - `DATABASE_POOL_TIMEOUT`
  - `DATABASE_POOL_RECYCLE`
  - `DATABASE_ECHO`
