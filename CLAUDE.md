# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## System Architecture

This is a **data-driven resume generator** that treats career information as structured JSON data and dynamically customizes resumes for specific job opportunities. The core philosophy separates content from presentation, enabling programmatic optimization.

### Core Components

**`resume_generator.py`** - Main application with three key functions:
- `ResumeGenerator.generate_ats_template()` - Renders structured data into HTML
- `extract_keywords_from_job_description()` - Analyzes job postings using regex patterns
- `customize_for_role()` - Reorders achievements by relevance score to job keywords

**Template System** - Embedded HTML generator with:
- ATS optimization via hidden keyword injection (`<div class="ats-keywords">`)
- Responsive Bootstrap CSS with FinTech-specific styling
- Achievement bullet points dynamically ordered by relevance

## Common Commands

```bash
# Default resume generation (most common use case)
python3 resume_generator.py
# Output: resume_ats_default_YYYYMMDD.html

# Job-specific customization
python3 resume_generator.py david_resume_json.json ats job_description.txt
# Output: resume_ats_customized_YYYYMMDD.html

# Alternative helper script
./generate_resume.sh [job_description.txt]

# ATS Testing and Optimization
./run_ats_tests.sh                    # Run comprehensive ATS test suite
./run_ats_tests.sh --verbose          # Detailed test output with analysis
python3 test_resume_suite.py          # Direct test suite execution
```

## Key Data Structures

**Achievement Object:**
```json
{
  "text": "Led wrapped token projects...",
  "keywords": ["defi", "tvl", "ethereum"],
  "metrics": {"value": 100000000, "type": "assets_managed"}
}
```

**Skills Hierarchy:**
```json
{
  "programming_languages": {
    "expert": ["C#", ".NET Core"],
    "proficient": ["Python", "JavaScript"]
  }
}
```

## Customization Algorithm

1. **Keyword Extraction**: Regex patterns prioritize FinTech terms (DeFi, blockchain, payments)
2. **Relevance Scoring**: Each achievement gets scored by keyword intersection with job description
3. **Dynamic Reordering**: Achievements sorted by `relevance_score` (descending) within each job
4. **ATS Injection**: Extracted keywords hidden in HTML for applicant tracking systems

## Development Notes

- Resume data uses semantic field names (`duration`, `company`, `achievements`) for maintainability
- HTML template is self-contained (embedded CSS) for portability
- Job description analysis focuses on requirement phrases ("required", "experience with", "proficient in")
- Error handling provides clear guidance for missing files and parameter usage

## ATS Testing Framework

The system includes a comprehensive automated testing suite for ATS optimization:

### Test Components
- **`test_resume_suite.py`**: Automated test framework with 5 job role scenarios
- **`test_job_descriptions/`**: Curated job descriptions for different FinTech roles
- **`run_ats_tests.sh`**: Convenience script for running all tests with analysis
- **`TEST_SUITE_DOCUMENTATION.md`**: Comprehensive testing documentation

### Performance Metrics
- **Average ATS Score**: 85.4% (target: 80%+)
- **Best Performance**: 95.3% (Engineering Manager - DeFi role)
- **Keyword Extraction**: 60 keywords per job description
- **Test Coverage**: 5 distinct job types with role-specific optimization

### Algorithm Enhancements
1. **Enhanced Keyword Extraction**: Weighted scoring, contextual analysis, technology stack detection
2. **Improved ATS Injection**: Skill variations, strategic repetition, enhanced coverage
3. **Smart Achievement Scoring**: Weighted relevance, partial matching, metrics bonus

### Testing Commands
```bash
./run_ats_tests.sh --verbose    # Full test suite with detailed analysis
python3 test_resume_suite.py    # Direct test execution
```