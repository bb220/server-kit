# server-kit

Modern web app starter.

## TODO
- [x] init project with `uv`
- [x] scaffold FastAPI app, async route handlers
- [x] configure ruff for linting/formatting checks
- [x] set up test suite
- [ ] CI/CD github workflow
- [ ] set up logging
- [ ] ORM + lite DB + migrations
- [ ] async for I/O operations
- [ ] integrate 3rd-party service

## Quickstart
```bash
uv sync
uv run fastapi dev src/server_kit/main.py
```

## Quality checks
```bash
uv run ruff check
uv run ruff format --check
```

## Tests
```bash
uv run pytest
uv run pytest -m integration
```
