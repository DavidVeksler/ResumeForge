# CLAUDE.md

Technical guidance for AI assistants (Claude Code) when working with this repository.

## System Architecture

ResumeForge is a **data-driven resume generator** that treats career information as structured JSON data and dynamically customizes resumes for specific job opportunities. The core philosophy separates content from presentation, enabling programmatic optimization.

### Technology Stack

**Backend (v2.0 - Consolidated Architecture):**
- Flask 3.0 REST API with CORS support
- **Single package structure** (`backend/`) with modular subpackages
- Centralized configuration with type hints throughout
- Provider abstraction layer for AI services (OpenAI API or Local LLM)
- Python 3.8+ with comprehensive type annotations

**Frontend:**
- React 18 with functional components and hooks
- Bootstrap 5 for responsive UI
- Axios for API communication
- Browser localStorage for data persistence

**AI Integration:**
- OpenAI API (gpt-4o-mini) for production
- Local LLM support via OpenAI-compatible endpoint (LM Studio)
- Abstracted provider interface for easy switching

### Core Components

#### Backend Services (v2.0)

**`backend/main.py`** - Single Entry Point
- Consolidated from `app.py`, `run_app.py`, `simple_server.py`
- Command-line argument parsing
- Startup configuration and health display

**`backend/api/routes.py`** - REST API Endpoints
- All consolidated API routes
- Request/response handling
- CORS configuration

**`backend/services/`** - Business Logic Layer
- `resume.py` - Resume generation and optimization
- `scoring.py` - ATS scoring algorithms
- `parsing.py` - Text-to-JSON conversion
- `validation.py` - Input validation

**`backend/providers/`** - AI Provider Abstraction
- `base.py` - Provider interface (abstract base class)
- `openai_provider.py` - OpenAI implementation
- `local_provider.py` - Local LLM implementation
- `factory.py` - Provider factory pattern

**`backend/models/`** - Data Models with Type Hints
- `resume.py` - Resume data structures
- `requests.py` - API request schemas
- `responses.py` - API response schemas
- `validation.py` - Validation result models

**`backend/config/settings.py`** - Centralized Configuration
- Environment variable management
- Application settings
- Feature flags

#### Frontend Components

**`src/components/LandingPage.js`**
- Professional landing page with value proposition
- Email capture and testimonials
- Feature showcase

**`src/components/TextResumeInput.js`**
- AI-powered text-to-JSON conversion interface
- Provider-agnostic API integration
- Real-time conversion feedback

**`src/components/Dashboard.js`**
- Main resume optimization interface
- File upload and job description input
- Results display with ATS scoring

**`src/utils/storage.js`**
- Browser localStorage management
- Auto-save functionality with debouncing
- Data expiration and cleanup

## Key Data Structures

### Resume JSON Schema

```json
{
  "personal": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "linkedin": "string",
    "github": "string"
  },
  "summary": {
    "headline": "string",
    "bullets": ["string"]
  },
  "experience": [
    {
      "title": "string",
      "company": "string",
      "duration": "string",
      "achievements": [
        {
          "text": "string",
          "keywords": ["string"],
          "metrics": {
            "value": number,
            "type": "string"
          },
          "relevance_score": number  // Added during optimization
        }
      ]
    }
  ],
  "skills": {
    "category_name": {
      "expert": ["string"],
      "proficient": ["string"],
      "familiar": ["string"]
    }
  },
  "education": [
    {
      "degree": "string",
      "school": "string",
      "year": "string",
      "details": "string"
    }
  ],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "technologies": ["string"],
      "link": "string"
    }
  ]
}
```

### Achievement Scoring

Each achievement object gets enhanced during optimization:

```python
{
    "text": "Led DeFi project managing $100M+ TVL...",
    "keywords": ["defi", "tvl", "ethereum"],
    "metrics": {"value": 100000000, "type": "assets_managed"},
    "relevance_score": 8.5  # 0-10 scale based on job description match
}
```

## Optimization Algorithm

### 1. Keyword Extraction
Located in `services/scoring_service.py`:

```python
def extract_keywords_from_job_description(job_description: str) -> set
```

**Process:**
- Regex patterns prioritize FinTech terms (DeFi, blockchain, payments, etc.)
- Extract from requirement phrases ("required", "experience with", "proficient in")
- Normalize to lowercase, remove duplicates
- Return 50-80 keywords per job description

**Enhancement Techniques:**
- Weighted scoring (required > preferred > nice-to-have)
- Contextual analysis (technology stack detection)
- Skill variation matching (React, ReactJS, React.js)

### 2. Relevance Scoring
Located in `services/resume_service.py`:

```python
def calculate_relevance_score(achievement: dict, keywords: set) -> float
```

**Scoring Factors:**
1. **Keyword Match** (70% weight): Count of job keywords in achievement text
2. **Partial Matching** (20% weight): Substring and fuzzy matches
3. **Metrics Bonus** (10% weight): Quantifiable achievements get boost

**Score Range:** 0-10, where 10 = perfect match

### 3. Dynamic Reordering
Achievements are sorted by `relevance_score` (descending) within each job entry, ensuring most relevant experience appears first.

### 4. ATS Keyword Injection
Hidden `<div class="ats-keywords">` elements injected into HTML with:
- Extracted job keywords
- Skill variations (e.g., "JavaScript", "JS", "ES6")
- Strategic repetition of high-value terms
- White text on white background (invisible to humans, visible to ATS)

## AI Provider System

### Configuration

Environment variables in `.env`:

```bash
# Provider Selection
AI_PROVIDER=openai  # or 'local'

# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Local LLM Configuration
LOCAL_LLM_BASE_URL=http://172.28.144.1:1234/v1
LOCAL_MODEL_NAME=local-model
```

### Provider Switching Logic (v2.0)

Located in `backend/providers/factory.py`:

```python
from backend.providers import create_ai_provider

# Automatically uses configured provider from settings
provider = create_ai_provider()  # Uses AI_PROVIDER env var

# Or explicitly specify
openai_provider = create_ai_provider('openai')
local_provider = create_ai_provider('local')
```

**Provider Interface:**
All providers implement the `AIProvider` abstract base class, ensuring consistent API:

```python
class AIProvider(ABC):
    @abstractmethod
    def parse_resume_text(text: str) -> Dict[str, Any]: ...

    @abstractmethod
    def test_connectivity() -> Dict[str, Any]: ...
```

**Frontend Compatibility:**
The React frontend (`TextResumeInput.js`) is provider-agnostic - it simply calls `/api/parse-resume` regardless of backend configuration.

### AI Prompting Strategy

Text-to-JSON conversion uses structured prompts:

```python
system_prompt = """Convert the following resume text into a JSON structure.
Extract personal information, work experience, skills, education, and projects.
Identify keywords for each achievement that would be relevant for job matching.
Format metrics numerically where possible."""
```

**Quality Assurance:**
- JSON schema validation on backend
- Error messages with specific field issues
- Retry logic for malformed responses

## Development Commands

### Common Workflows (v2.0)

```bash
# Full application start
./start.sh                          # Single command (combined)
./start_backend.sh                  # Backend only (dev mode, uses backend/main.py)
./start_frontend.sh                 # Frontend only (hot-reload)

# Direct backend execution (NEW in v2.0)
python3 -m backend.main             # Default settings
python3 -m backend.main --port 8000 # Custom port
python3 -m backend.main --debug     # Enable debug mode

# Environment setup
./setup_dev.sh                      # Validate environment
./install_dependencies.sh           # Install all dependencies
./install_pdf_support.sh            # PDF export support (wkhtmltopdf)

# Testing (NEW consolidated test suite)
pytest backend/tests/               # Run all tests
pytest backend/tests/test_api.py    # API tests only
pytest backend/tests/test_services.py  # Service layer tests
pytest backend/tests/test_providers.py # Provider tests

# Legacy tests (still available for compatibility)
python3 test_ai_providers.py        # Test both AI providers
python3 basic_integration_test.py   # Core functionality test

# Command-line resume generation
python3 resume_generator.py         # Default resume
python3 resume_generator.py david_resume_json.json ats job_description.txt
```

### Testing Framework (v2.0)

**NEW: Consolidated Test Suite** (`backend/tests/`):
- `test_api.py` - API endpoint tests with Flask test client
- `test_services.py` - Business logic and service layer tests
- `test_providers.py` - AI provider implementation tests
- `conftest.py` - Shared pytest fixtures and configuration

**Test Execution:**
```bash
# All tests
pytest backend/tests/

# With coverage
pytest backend/tests/ --cov=backend --cov-report=html

# Specific test file
pytest backend/tests/test_api.py -v
```

**Legacy Tests** (still available):
- `test_ai_providers.py` - Standalone AI provider tests
- `basic_integration_test.py` - Core functionality validation

## API Endpoints Reference

### Core Endpoints

**GET `/api/health`**
- Returns backend status and AI provider configuration
- No authentication required
- Response includes Python version, Flask version, AI provider

**POST `/api/optimize`**
- Main resume optimization endpoint
- Request body: `{ "resume": {...}, "job_description": "..." }`
- Returns optimized resume with relevance scores and ATS metrics

**POST `/api/parse-resume`**
- AI-powered text-to-JSON conversion
- Request body: `{ "resume_text": "..." }`
- Uses configured AI provider (transparent to frontend)
- Returns structured JSON resume

**POST `/api/validate-resume`**
- Validates resume JSON structure
- Checks for required fields and data types
- Returns validation errors with specific field paths

**GET `/api/sample-resume`**
- Downloads sample resume template
- Returns JSON file with example structure
- Includes all fields and formatting guidelines

**POST `/api/export-pdf`**
- Generates PDF from optimized HTML resume
- Requires wkhtmltopdf installed
- Returns PDF file for download

## File Organization

### Backend Structure (v2.0 - Consolidated)
```
ResumeForge/
├── backend/                    # NEW: Single consolidated package
│   ├── __init__.py
│   ├── main.py                # Single entry point (replaces app.py, run_app.py, simple_server.py)
│   │
│   ├── api/                   # API layer
│   │   ├── __init__.py
│   │   ├── routes.py         # All REST API endpoints
│   │   └── health.py         # Health check utilities
│   │
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   ├── resume.py         # Resume generation and optimization
│   │   ├── scoring.py        # ATS scoring algorithms
│   │   ├── parsing.py        # Text-to-JSON conversion
│   │   └── validation.py     # Input validation
│   │
│   ├── providers/             # AI provider abstraction
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract provider interface
│   │   ├── openai_provider.py # OpenAI implementation
│   │   ├── local_provider.py  # Local LLM implementation
│   │   └── factory.py        # Provider factory
│   │
│   ├── models/                # Data models with type hints
│   │   ├── __init__.py
│   │   ├── resume.py         # Resume data structures
│   │   ├── requests.py       # API request schemas
│   │   ├── responses.py      # API response schemas
│   │   └── validation.py     # Validation models
│   │
│   ├── config/                # Centralized configuration
│   │   ├── __init__.py
│   │   └── settings.py       # Application settings (from env vars)
│   │
│   └── tests/                 # Consolidated test suite
│       ├── __init__.py
│       ├── conftest.py       # Pytest configuration
│       ├── test_api.py       # API endpoint tests
│       ├── test_services.py  # Service layer tests
│       └── test_providers.py # Provider tests
│
├── resume/                    # Legacy resume generation (still used)
│   ├── generator.py          # HTML template generation
│   ├── keyword_extractor.py  # Job description analysis
│   └── relevance_scorer.py   # Achievement scoring
│
├── config/                    # Legacy config (still used)
│   └── patterns.py           # Regex patterns for keywords
│
├── resume_generator.py        # CLI tool (still available)
└── [Legacy files - kept for compatibility]
    ├── app.py                # OLD: Replaced by backend/main.py
    ├── run_app.py            # OLD: Replaced by backend/main.py
    └── simple_server.py      # OLD: Replaced by backend/main.py
```

### Frontend Structure
```
src/
├── App.js                     # Main React app with routing
├── index.js                   # React entry point
│
├── components/
│   ├── LandingPage.js        # Landing page
│   ├── Dashboard.js          # Main optimization UI
│   ├── TextResumeInput.js    # AI conversion interface
│   ├── FileUpload.js         # JSON file upload
│   ├── InputSection.js       # Job description input
│   ├── ResultsSection.js     # Optimization results
│   ├── ResumeDisplay.js      # HTML resume preview
│   └── StorageDebugger.js    # localStorage management
│
├── services/
│   └── api.js                # Axios API wrapper
│
└── utils/
    └── storage.js            # localStorage utilities
```

## Performance Optimization

### Backend
- Modular service architecture for code splitting
- Efficient keyword matching with set operations
- Minimal dependencies (Flask, CORS, dotenv, OpenAI)
- JSON validation with early returns

### Frontend
- React component memoization where needed
- Debounced auto-save (2 second delay)
- Lazy loading for heavy components
- Optimized Bootstrap bundle (production build)

### AI Integration
- gpt-4o-mini for cost-effective conversions (~$0.15-0.60/1K tokens)
- Structured prompts for consistent JSON output
- Retry logic with exponential backoff
- Local LLM option for zero API cost

## Production Deployment

See `DEPLOYMENT.md` for complete Ubuntu server setup with:
- Systemd service configuration
- Nginx reverse proxy
- SSL/TLS with Let's Encrypt
- Process management and auto-restart
- Log aggregation and monitoring

Quick deploy:
```bash
./deploy.sh
```

## Development Best Practices

### Adding New Features (v2.0)

1. **Backend Service**: Add logic in `backend/services/` directory
2. **API Route**: Add endpoint in `backend/api/routes.py`
3. **Data Models**: Define schemas in `backend/models/` with type hints
4. **Frontend**: Create component in `src/components/`
5. **API Client**: Update `src/services/api.js` with new endpoint
6. **Testing**: Add tests in `backend/tests/` using pytest
7. **Documentation**: Update CLAUDE.md, README.md, and backend/README.md

**Example: Adding a New AI Provider**
1. Create `backend/providers/your_provider.py` implementing `AIProvider`
2. Update `backend/providers/factory.py` to recognize new provider
3. Add tests in `backend/tests/test_providers.py`
4. Update `.env.example` with new provider configuration

### Code Style

- **Python**: PEP 8 style guide, type hints encouraged
- **JavaScript**: ES6+ features, functional components
- **Error Handling**: Descriptive messages with specific field references
- **Logging**: Use Flask logger for backend, console for frontend dev

### Git Workflow

- **Main branch**: Production-ready code
- **Feature branches**: `claude/*` prefix for AI-assisted development
- **Commits**: Descriptive messages focusing on "why" not "what"
- **Pull Requests**: Include summary and test plan

## Common Development Tasks

### Adding a New AI Provider

1. Update `app.py` to handle new provider type
2. Add provider configuration to `.env.example`
3. Create test in `test_ai_providers.py`
4. Update documentation (this file and README.md)

### Modifying Optimization Algorithm

1. Edit `services/scoring_service.py` for keyword logic
2. Edit `services/resume_service.py` for relevance scoring
3. Update tests in `basic_integration_test.py`
4. Test with multiple job descriptions

### Adding New Resume Field

1. Update JSON schema in `services/resume_service.py`
2. Update validation logic
3. Update HTML template in `resume/generator.py`
4. Update React components for display
5. Update sample resume (`david_resume_json.json`)

## Troubleshooting

### AI Provider Issues

**OpenAI API errors:**
- Check API key validity: `python3 test_ai_providers.py`
- Verify model availability (gpt-4o-mini)
- Check rate limits and billing status

**Local LLM errors:**
- Ensure LM Studio is running: `curl http://172.28.144.1:1234/v1/models`
- Verify model is loaded in LM Studio
- Check base URL in `.env` matches server address

### Port Conflicts

**Backend (5000):**
```bash
lsof -i :5000          # Find process using port
kill -9 <PID>          # Kill process if needed
```

**Frontend (3000):**
```bash
lsof -i :3000
kill -9 <PID>
```

### Dependency Issues

**Python:**
```bash
pip3 list                              # List installed packages
pip3 install -r requirements.txt --user  # Reinstall
```

**Node.js:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **React Documentation**: https://react.dev/
- **OpenAI API**: https://platform.openai.com/docs
- **LM Studio**: https://lmstudio.ai/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/

## Current Configuration

**Production Setup:**
- AI Provider: OpenAI API (gpt-4o-mini)
- Backend: Flask development server (port 5000)
- Frontend: React development server (port 3000)
- Data: Browser localStorage (5MB quota)

**Next Steps for Production:**
- Enable SSL/TLS via Let's Encrypt
- Configure Nginx reverse proxy
- Set up systemd services
- Implement rate limiting
- Add monitoring and logging

---

**Note:** This file is specifically for AI assistants working on the codebase. For end-user documentation, see `README.md`.
