# ResumeForge

AI-powered resume optimizer that uses intelligent keyword matching and ATS (Applicant Tracking System) optimization to maximize interview callbacks.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key (for AI text-to-JSON conversion) **OR** Local LLM setup

### 1. Install & Configure

```bash
# Clone the repository
git clone https://github.com/DavidVeksler/ResumeForge
cd ResumeForge

# Install dependencies
./install_dependencies.sh

# Configure AI provider
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY or configure local LLM
```

### 2. Start the Application

**Option A: Simple One-Command Start**
```bash
./start.sh
```
This starts both backend and frontend in a single terminal.

**Option B: Separate Terminals (Recommended for Development)**
```bash
# Terminal 1: Backend
./start_backend.sh

# Terminal 2: Frontend
./start_frontend.sh
```

### 3. Open the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Features

### Resume Optimization
- **Smart Keyword Matching**: Analyzes job descriptions and reorders achievements by relevance
- **ATS Score Tracking**: Compare default vs. optimized resume scores
- **Achievement Ranking**: Dynamically prioritizes your most relevant experience

### Resume Input Methods
- **JSON Upload**: Structured resume data for precise control
- **AI Text-to-JSON Conversion**: Paste any text resume and convert it automatically
- **Sample Templates**: Download example resume format

### Export Options
- PDF export (requires wkhtmltopdf)
- HTML download
- Print-ready formatting

### Modern Web Interface
- Professional landing page
- Real-time validation
- Auto-save functionality
- Responsive design (mobile/tablet/desktop)

## AI Provider Configuration

ResumeForge supports two AI providers for text-to-JSON conversion:

### OpenAI API (Recommended)
```bash
# In .env file:
AI_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

**Benefits:**
- High accuracy (~3-5 seconds per conversion)
- No local setup
- Production-ready
- Cost: ~$0.15-0.60 per 1K tokens

### Local LLM (Privacy & Offline)
```bash
# In .env file:
AI_PROVIDER=local
LOCAL_LLM_BASE_URL=http://172.28.144.1:1234/v1
LOCAL_MODEL_NAME=local-model
```

**Benefits:**
- Complete privacy
- No API costs
- Offline operation

**Requirements:**
1. Install [LM Studio](https://lmstudio.ai/)
2. Download a model (Llama 3.1, Mistral, etc.)
3. Start local server

## Project Structure

```
ResumeForge/
├── app.py                    # Flask REST API server
├── resume_generator.py       # Core resume processing engine
├── run_app.py               # Application runner
├──
├── src/                     # React frontend
│   ├── components/          # UI components
│   ├── services/           # API integration
│   └── utils/              # Storage management
│
├── services/               # Backend services
│   ├── ai_service.py       # AI provider integration
│   ├── resume_service.py   # Resume processing
│   └── scoring_service.py  # ATS scoring
│
├── Startup Scripts
│   ├── start.sh            # Quick start (combined)
│   ├── start_backend.sh    # Backend only
│   ├── start_frontend.sh   # Frontend only
│   ├── setup_dev.sh        # Environment validation
│   └── install_dependencies.sh
│
└── Documentation
    ├── README.md           # This file
    ├── CLAUDE.md          # Technical architecture
    └── DEPLOYMENT.md      # Production deployment
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check & configuration status |
| `/api/optimize` | POST | Optimize resume for job description |
| `/api/parse-resume` | POST | AI text-to-JSON conversion |
| `/api/validate-resume` | POST | Validate resume structure |
| `/api/sample-resume` | GET | Download sample template |
| `/api/export-pdf` | POST | Generate PDF export |

## Command-Line Usage

For quick resume generation without the web interface:

```bash
# Generate default resume
python3 resume_generator.py

# Generate job-specific resume
python3 resume_generator.py david_resume_json.json ats job_description.txt
```

## Testing

```bash
# Validate environment setup
./setup_dev.sh

# Test AI providers
python3 test_ai_providers.py

# Basic integration test
python3 basic_integration_test.py

# Full integration test (requires OpenAI API)
python3 integration_test.py
```

## Resume JSON Format

Your resume should be structured with these sections:
- `personal`: Contact information
- `summary`: Professional summary with headline and bullets
- `experience`: Work history with achievements and keywords
- `skills`: Technical skills by category and proficiency
- `education`: Educational background
- `projects`: Key projects (optional)

Use the **"Download Sample Template"** button in the app for a complete example.

## Performance Metrics

- **Keyword Processing**: 50+ keywords per job description
- **ATS Score Improvement**: Typical 10-15% (up to 30% in optimized cases)
- **Response Time**: <3 seconds for optimization
- **AI Conversion**: <30 seconds for text-to-JSON

## Technology Stack

- **Backend**: Flask, Python 3.8+
- **Frontend**: React 18, Bootstrap 5
- **AI Integration**: OpenAI API or Local LLM
- **PDF Generation**: wkhtmltopdf + pdfkit
- **Data Persistence**: Browser localStorage with auto-save

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python3 --version

# Reinstall dependencies
./install_dependencies.sh

# Check if port 5000 is in use
lsof -i :5000
```

### Frontend won't start
```bash
# Check Node.js version
node --version

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Resume generation fails
```bash
# Validate environment
./setup_dev.sh

# Test core functionality
python3 basic_integration_test.py
```

### AI conversion not working
```bash
# Check .env configuration
cat .env

# Verify OpenAI API key
python3 test_ai_providers.py

# Check API health
curl http://localhost:5000/api/health
```

## Production Deployment

Ready for Ubuntu server deployment with systemd services, Nginx, and SSL.

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete production setup instructions.

```bash
# Quick deploy to Ubuntu server
./deploy.sh
```

## Development

### Start Development Environment
```bash
# Validate setup
./setup_dev.sh

# Start with hot-reload
./start_backend.sh  # Terminal 1
./start_frontend.sh # Terminal 2
```

### Tech Stack Details
- **Architecture**: Full-stack web app with REST API
- **Frontend**: React with React Router, Axios for API calls
- **Backend**: Flask with CORS support, modular service architecture
- **AI**: Configurable provider system (OpenAI/Local)
- **Styling**: Bootstrap 5 + custom CSS with Inter font
- **Validation**: Multi-layer client and server-side validation

## Contributing

This is a personal project, but feedback and suggestions are welcome via GitHub issues.

## License

MIT License - see LICENSE file for details.

## Author

David Veksler - [GitHub](https://github.com/DavidVeksler)
