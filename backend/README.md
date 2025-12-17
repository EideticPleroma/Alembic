# Alembic Backend

FastAPI-based backend for the Alembic Hermetic tarot reading application.

## Quick Start

### Prerequisites

- Python 3.11+
- pip or uv package manager

### Setup

```bash
# Clone and navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (including dev tools)
pip install -e ".[dev]"

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

### Run the Server

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

View interactive API docs at `http://localhost:8000/docs`

### Verify Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "checks": {
    "database": null,
    "llm": null,
    "stripe": null
  },
  "timestamp": "2025-12-16T14:30:00+00:00"
}
```

## Development

### Code Quality

All code quality checks run automatically via pre-commit hooks on commit:

```bash
# Manual lint check
ruff check .

# Manual format check
ruff format --check .

# Manual type checking
mypy app

# Manual tests
pytest -v
```

### Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_health.py

# Run with coverage report
pytest --cov=app --cov-report=html
```

Test structure:
- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests (coming in later phases)
- `tests/conftest.py` - Shared pytest fixtures

### Pre-commit Hooks

Pre-commit hooks run automatically when you commit. They ensure:
- Code formatting via Ruff
- Type checking via MyPy
- All tests pass

Install pre-commit hooks:

```bash
pre-commit install
```

Run hooks manually:

```bash
pre-commit run --all-files
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings via pydantic-settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependency injection
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── health.py       # Health check endpoint
│   └── core/
│       ├── __init__.py
│       └── tarot/
│           ├── __init__.py
│           └── data/
│               └── cards.json  # 78-card tarot deck
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_health.py
│   │   └── test_config.py
│   ├── integration/
│   │   └── __init__.py
│   └── fixtures/
├── .env.example                # Environment template
├── .pre-commit-config.yaml     # Pre-commit hooks
├── pyproject.toml              # Project metadata & tool config
└── README.md                   # This file
```

## Configuration

Settings are loaded from environment variables via `app/config.py`.

### Required Variables

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

### Optional Variables

```bash
# LLM (choose one)
XAI_API_KEY=xai-xxx              # For production Grok
USE_LOCAL_LLM=false              # Or set true for Ollama

# Stripe (for payment features)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Application
ENVIRONMENT=development           # development, staging, production
DEBUG=false
LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR
CORS_ORIGINS=http://localhost:3000
```

See `env.example` for complete reference.

## API Endpoints

### Phase 0 (Foundation)

- `GET /health` - Health check status

More endpoints coming in Phase 1 (Reading flows).

Full API design documented at `docs/architecture/api-design.md`

## Development Workflow

### Making Changes

1. Create a new branch for your feature
2. Make changes and add tests
3. Ensure all quality checks pass:
   ```bash
   ruff check .
   ruff format --check .
   mypy app
   pytest -v
   ```
4. Commit (pre-commit hooks will run automatically)
5. Push and create a pull request

### Adding a New Endpoint

1. Create router in `app/api/routers/`
2. Import and include router in `app/main.py`
3. Write tests in `tests/unit/`
4. Document in API design docs

### Adding a New Dependency

1. Update `pyproject.toml` in the appropriate section
2. Run `pip install -e ".[dev]"`
3. Use in code

## Troubleshooting

### Port 8000 Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Import Errors

```bash
# Ensure dev dependencies installed
pip install -e ".[dev]"

# Reinstall in editable mode
pip install -e . --force-reinstall
```

### Type Checking Fails

```bash
# Update type stubs
pip install --upgrade types-stripe
```

### Tests Won't Run

```bash
# Check pytest is installed
pytest --version

# Run with verbose output to see errors
pytest -vv
```

## Deployment

See `docs/guides/deployment.md` for production deployment instructions.

## Next Steps

- Phase 1: Tarot deck and spread logic
- Phase 2: User authentication and persistence
- Phase 3: Conversational follow-up via LLM
- Phase 4: Stripe monetization integration

See `docs/PROJECT-PLAN.md` for full roadmap.

## License

MIT
