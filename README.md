# server-kit

Starter for modern API server projects.

### Tech Stack
| Description | Name |
| --- | --- |
| Language/runtime | [Python](https://www.python.org/) |
| Web framework and server | [FastAPI](https://fastapi.tiangolo.com/) (+ [Uvicorn](https://www.uvicorn.org/))|
| Test framework | [Pytest](https://docs.pytest.org/) |
| Linting and formatting tool | [Ruff](https://docs.astral.sh/ruff/) |
| Dependency management and task runner | [uv](https://docs.astral.sh/uv/) |

## TODO
- [x] init project with `uv`
- [x] scaffold FastAPI app, async route handlers
- [x] configure ruff for linting/formatting checks
- [x] set up test suite
- [x] CI/CD github workflow
- [ ] set up logging
- [ ] ORM + lite DB + migrations
- [ ] async for I/O operations
- [ ] integrate 3rd-party service

## Quickstart
```bash
uv sync
uv run fastapi dev src/server_kit/main.py
```

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
