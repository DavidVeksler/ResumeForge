# ResumeForge Backend v2.0

**Consolidated Python application with modular architecture**

## Overview

This is the refactored backend for ResumeForge, consolidating multiple scattered modules (`app.py`, `run_app.py`, `simple_server.py`, etc.) into a single coherent Python package.

## Architecture

```
backend/
├── __init__.py              # Package initialization
├── main.py                  # Single entry point (replaces app.py, run_app.py, simple_server.py)
├── api/                     # API routes and endpoints
│   ├── routes.py           # All REST API endpoints
│   └── health.py           # Health check utilities
├── services/                # Business logic layer
│   ├── resume.py           # Resume generation and optimization
│   ├── scoring.py          # ATS scoring algorithms
│   ├── parsing.py          # Text-to-JSON conversion
│   └── validation.py       # Input validation
├── providers/               # AI provider implementations
│   ├── base.py             # Base provider interface
│   ├── openai_provider.py  # OpenAI implementation
│   ├── local_provider.py   # Local LLM implementation
│   └── factory.py          # Provider factory
├── models/                  # Data models with type hints
│   ├── resume.py           # Resume data structures
│   ├── requests.py         # API request models
│   ├── responses.py        # API response models
│   └── validation.py       # Validation result models
├── config/                  # Centralized configuration
│   └── settings.py         # Application settings
└── tests/                   # Consolidated test suite
    ├── test_api.py         # API endpoint tests
    ├── test_services.py    # Service layer tests
    └── test_providers.py   # AI provider tests
```

## Key Improvements

### Before (v1.x)
- **Multiple entry points**: `app.py`, `run_app.py`, `simple_server.py`
- **Scattered configuration**: Environment variables, hardcoded values, settings files
- **Duplicated logic**: AI provider code in multiple places
- **No type hints**: Limited type safety
- **Tests in root**: Disorganized test files

### After (v2.0)
- ✅ **Single entry point**: `backend/main.py`
- ✅ **Centralized config**: `backend/config/settings.py`
- ✅ **Provider abstraction**: `backend/providers/` with factory pattern
- ✅ **Type hints**: Full typing throughout codebase
- ✅ **Organized tests**: `backend/tests/` with pytest structure

## Running the Backend

### Quick Start

```bash
# From project root
python3 -m backend.main
```

### With Custom Options

```bash
# Custom port
python3 -m backend.main --port 8000

# Enable debug mode
python3 -m backend.main --debug

# Custom host
python3 -m backend.main --host 0.0.0.0 --port 8080
```

### Using Startup Scripts

```bash
# Backend only
./start_backend.sh

# Both backend and frontend
./start.sh
```

## Configuration

All configuration is centralized in `backend/config/settings.py` and loaded from environment variables:

```bash
# .env file
AI_PROVIDER=openai              # or 'local'
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

LOCAL_LLM_BASE_URL=http://localhost:1234/v1
LOCAL_MODEL_NAME=local-model

FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check with system info |
| POST | `/api/optimize` | Optimize resume for job description |
| POST | `/api/parse-resume` | Convert text resume to JSON (AI) |
| POST | `/api/validate-resume` | Validate resume structure |
| GET | `/api/sample-resume` | Get sample resume template |
| POST | `/api/export-pdf` | Export resume as PDF |

## Development

### Running Tests

```bash
# All tests
pytest backend/tests/

# Specific test file
pytest backend/tests/test_api.py

# With coverage
pytest backend/tests/ --cov=backend --cov-report=html
```

### Code Structure

**Services Layer** (`backend/services/`)
- Contains all business logic
- No direct Flask dependencies
- Reusable across different interfaces

**API Layer** (`backend/api/`)
- Flask route handlers
- Request/response transformation
- Error handling

**Providers Layer** (`backend/providers/`)
- Abstraction for AI providers
- Easy to add new providers
- Factory pattern for instantiation

**Models Layer** (`backend/models/`)
- Data structures with type hints
- Request/response schemas
- Validation models

## Migration from v1.x

### Old vs New Entry Points

| Old | New |
|-----|-----|
| `python3 app.py` | `python3 -m backend.main` |
| `python3 run_app.py` | `python3 -m backend.main` |
| `python3 simple_server.py` | `python3 -m backend.main` |

### Old vs New Imports

```python
# Old
from services.ai_service import AIService
from services.resume_service import ResumeService

# New
from backend.services import ParsingService, ResumeService
from backend.providers import create_ai_provider
```

### Old vs New Tests

```bash
# Old
python3 integration_test.py
python3 test_ai_providers.py
python3 test_mock_api.py

# New
pytest backend/tests/
```

## Adding New Features

### Adding a New AI Provider

1. Create provider in `backend/providers/your_provider.py`:
```python
from .base import AIProvider

class YourProvider(AIProvider):
    # Implement required methods
    pass
```

2. Update factory in `backend/providers/factory.py`

3. Add tests in `backend/tests/test_providers.py`

### Adding a New Endpoint

1. Add route in `backend/api/routes.py`:
```python
@app.route("/api/your-endpoint", methods=["POST"])
def your_endpoint():
    # Implementation
    pass
```

2. Add service logic in appropriate `backend/services/` file

3. Add tests in `backend/tests/test_api.py`

## Troubleshooting

### Import Errors

If you see import errors, make sure you're running from the project root:

```bash
# Correct
cd /path/to/ResumeForge
python3 -m backend.main

# Wrong
cd /path/to/ResumeForge/backend
python3 main.py  # This won't work
```

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill it
lsof -ti:5000 | xargs kill -9
```

### AI Provider Errors

```bash
# Test OpenAI
python3 -c "from backend.providers import create_ai_provider; p = create_ai_provider('openai'); print(p.test_connectivity())"

# Test Local LLM
python3 -c "from backend.providers import create_ai_provider; p = create_ai_provider('local'); print(p.test_connectivity())"
```

## Future Enhancements

- [ ] FastAPI migration for async support
- [ ] Database integration (PostgreSQL)
- [ ] Caching layer (Redis)
- [ ] API authentication (JWT)
- [ ] Rate limiting
- [ ] Webhook support
- [ ] GraphQL API

---

**Version**: 2.0.0
**Last Updated**: 2025-11-22
