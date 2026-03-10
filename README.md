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

## Configuration
- Config is loaded from the env
- Local config can be loaded from `.env`
  - Copy `.env.example` and adjust values.
