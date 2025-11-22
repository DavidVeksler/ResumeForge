# Migration Guide: v1.x → v2.0

## Overview

ResumeForge v2.0 introduces a **consolidated backend architecture** that eliminates drift between multiple server entry points and provides a single, coherent Python package structure.

## What Changed

### Before (v1.x)
```
❌ Multiple entry points: app.py, run_app.py, simple_server.py
❌ Scattered configuration across environment variables and hardcoded values
❌ AI provider logic duplicated in multiple places
❌ Limited type hints
❌ Tests scattered in root directory
```

### After (v2.0)
```
✅ Single entry point: backend/main.py
✅ Centralized configuration: backend/config/settings.py
✅ Provider abstraction: backend/providers/ with factory pattern
✅ Comprehensive type hints throughout
✅ Organized test suite: backend/tests/
```

## Breaking Changes

### 1. Server Entry Point

**Old:**
```bash
python3 app.py
python3 run_app.py
python3 simple_server.py
```

**New:**
```bash
python3 -m backend.main
python3 -m backend.main --port 8000
python3 -m backend.main --debug
```

### 2. Imports

**Old:**
```python
from services.ai_service import AIService
from services.resume_service import ResumeService
```

**New:**
```python
from backend.services import ParsingService, ResumeService
from backend.providers import create_ai_provider
```

### 3. Tests

**Old:**
```bash
python3 integration_test.py
python3 test_ai_providers.py
```

**New:**
```bash
pytest backend/tests/
pytest backend/tests/test_api.py
```

## Migration Steps

### For End Users

**No changes required!** The frontend and startup scripts (`./start.sh`, `./start_backend.sh`) have been updated to use the new backend automatically.

### For Developers

1. **Update imports** in any custom scripts:
   ```python
   # Old
   from services.ai_service import AIService

   # New
   from backend.services import ParsingService
   from backend.providers import create_ai_provider
   ```

2. **Use new entry point** for manual server starts:
   ```bash
   python3 -m backend.main
   ```

3. **Run tests** with pytest:
   ```bash
   pytest backend/tests/
   ```

## Backward Compatibility

### Legacy Files Preserved

The following files are kept for compatibility but are **deprecated**:

- `app.py` → Use `backend/main.py` instead
- `run_app.py` → Use `backend/main.py` instead
- `simple_server.py` → Use `backend/main.py` instead
- `services/ai_service.py` → Use `backend/providers/` instead
- `services/resume_service.py` → Use `backend/services/resume.py` instead
- `services/scoring_service.py` → Use `backend/services/scoring.py` instead

### What Still Works

- ✅ Startup scripts (`./start.sh`, `./start_backend.sh`)
- ✅ CLI resume generator (`resume_generator.py`)
- ✅ Frontend React application (no changes needed)
- ✅ API endpoints (same URLs, same behavior)
- ✅ Environment variables (`.env` file format unchanged)

## New Features in v2.0

### 1. Provider Factory Pattern

```python
from backend.providers import create_ai_provider

# Uses AI_PROVIDER from environment
provider = create_ai_provider()

# Or explicitly specify
openai_provider = create_ai_provider('openai')
local_provider = create_ai_provider('local')
```

### 2. Type Hints Throughout

All models, services, and API handlers now have comprehensive type hints:

```python
from backend.models import OptimizeRequest, OptimizeResponse
from typing import Dict, Any

def process_resume(data: Dict[str, Any]) -> OptimizeResponse:
    # Fully typed
    pass
```

### 3. Centralized Settings

```python
from backend.config import settings

print(settings.ai.provider)  # 'openai' or 'local'
print(settings.flask.port)   # 5000
print(settings.pdf_export_enabled)  # True/False
```

### 4. Organized Tests

```bash
backend/tests/
├── test_api.py         # API endpoint tests
├── test_services.py    # Business logic tests
├── test_providers.py   # AI provider tests
└── conftest.py         # Shared fixtures
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError: No module named 'backend'`:

```bash
# Make sure you're in the project root
cd /path/to/ResumeForge

# Run from root, not from backend/
python3 -m backend.main
```

### Port Already in Use

```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Flask Not Found

The new backend gracefully handles missing Flask:

```bash
pip3 install -r requirements.txt --user
```

## Getting Help

- **Documentation**: See `backend/README.md` for detailed backend docs
- **Examples**: Check `backend/tests/` for usage examples
- **Issues**: Report bugs at GitHub issues

## Timeline

- **v1.x**: Legacy architecture (deprecated but still works)
- **v2.0**: Current consolidated architecture
- **v2.1+**: FastAPI migration, database integration (planned)

---

**Version**: 2.0.0
**Date**: 2025-11-22
