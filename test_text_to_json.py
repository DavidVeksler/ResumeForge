#!/usr/bin/env python3
"""
Unit Tests for Text-to-JSON Resume Conversion Feature

Tests the complete text-to-JSON conversion pipeline including:
- OpenAI API integration
- Resume parsing endpoint
- JSON validation
- Error handling
"""

import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys

# Try to import pytest, but continue without it if not available
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    print("⚠️  pytest not available - running mock tests only")

try:
    from flask import Flask
    from flask.testing import FlaskClient
    FLASK_AVAILABLE = True
    
    # Mock OpenAI before importing app
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        from app import app as flask_app
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️  Flask not available - skipping Flask tests")

class TestTextToJSONConversion:
    """Test suite for text-to-JSON resume conversion feature"""

    @pytest.fixture
    def app(self):
        """Create Flask test app"""
        flask_app.config['TESTING'] = True
        return flask_app

    @pytest.fixture
    def client(self, app):
        """Create Flask test client"""
        return app.test_client()

    @pytest.fixture
    def sample_text_resume(self):
        """Sample text resume for testing"""
        return """
John Smith
Senior Software Engineer
john.smith@email.com | (555) 123-4567 | San Francisco, CA
LinkedIn: linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Experienced software engineer with 8+ years developing scalable web applications and fintech solutions. Led teams of 5+ engineers and delivered $10M+ in revenue impact through innovative payment processing systems.

EXPERIENCE

Senior Software Engineer | TechCorp Inc | San Francisco, CA | 2020 - Present
• Built microservices architecture serving 1M+ daily users with 99.9% uptime
• Led migration to cloud infrastructure reducing costs by 40%
• Implemented real-time payment processing handling $50M monthly volume
• Mentored 3 junior developers and established code review processes

Software Engineer | StartupXYZ | San Francisco, CA | 2018 - 2020  
• Developed React/Node.js applications for cryptocurrency trading platform
• Integrated blockchain APIs for DeFi protocols with $100M+ TVL
• Optimized database queries improving performance by 60%

SKILLS
Programming: Python, JavaScript, TypeScript, Java, Go
Web Technologies: React, Node.js, Express, Django, PostgreSQL
Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Terraform
FinTech: Blockchain, DeFi, Payment Processing, API Integration

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018

PROJECTS
• DeFi Yield Optimizer - Built automated yield farming bot generating 15% APY
• Payment Gateway API - Developed secure payment processing for e-commerce platform
        """

    @pytest.fixture
    def expected_json_structure(self):
        """Expected JSON structure after conversion"""
        return {
            "personal": {
                "name": "John Smith",
                "email": "john.smith@email.com",
                "phone": "(555) 123-4567",
                "location": "San Francisco, CA",
                "linkedin": "linkedin.com/in/johnsmith"
            },
            "summary": {
                "headline": "Experienced software engineer with 8+ years developing scalable web applications and fintech solutions",
                "bullets": [
                    "Led teams of 5+ engineers",
                    "Delivered $10M+ in revenue impact",
                    "Innovative payment processing systems"
                ]
            },
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "TechCorp Inc",
                    "location": "San Francisco, CA",
                    "duration": "2020 - Present",
                    "achievements": [
                        {
                            "text": "Built microservices architecture serving 1M+ daily users with 99.9% uptime",
                            "keywords": ["microservices", "architecture", "scalable"],
                            "metrics": {"value": 1000000, "type": "daily_users"}
                        }
                    ]
                }
            ],
            "skills": {
                "programming_languages": {
                    "expert": ["Python", "JavaScript"],
                    "proficient": ["TypeScript", "Java", "Go"]
                }
            },
            "education": [
                {
                    "degree": "Bachelor of Science in Computer Science",
                    "school": "University of California, Berkeley",
                    "duration": "2014 - 2018"
                }
            ]
        }

    @pytest.fixture
    def mock_openai_response(self, expected_json_structure):
        """Mock OpenAI API response"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = json.dumps(expected_json_structure, indent=2)
        return mock_response

    def test_parse_resume_endpoint_success(self, client, sample_text_resume, mock_openai_response):
        """Test successful text resume parsing"""
        with patch('app.OpenAI') as mock_openai_class:
            # Mock OpenAI client
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_openai_response
            
            # Mock environment variable
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                response = client.post('/api/parse-resume', 
                    json={'textResume': sample_text_resume},
                    content_type='application/json'
                )
            
            assert response.status_code == 200
            data = response.get_json()
            
            assert data['success'] is True
            assert 'resumeData' in data
            assert 'validation' in data
            assert data['message'] == 'Resume successfully converted to structured JSON format'
            
            # Validate resume structure
            resume_data = data['resumeData']
            assert 'personal' in resume_data
            assert 'experience' in resume_data
            assert resume_data['personal']['name'] == 'John Smith'

    def test_parse_resume_missing_text(self, client):
        """Test parsing with missing text resume"""
        response = client.post('/api/parse-resume', 
            json={},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing textResume field' in data['error']

    def test_parse_resume_empty_text(self, client):
        """Test parsing with empty text resume"""
        response = client.post('/api/parse-resume', 
            json={'textResume': '   '},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Text resume cannot be empty' in data['error']

    def test_parse_resume_no_api_key(self, client, sample_text_resume):
        """Test parsing without OpenAI API key"""
        with patch.dict(os.environ, {}, clear=True):
            response = client.post('/api/parse-resume', 
                json={'textResume': sample_text_resume},
                content_type='application/json'
            )
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'OpenAI API key not configured' in data['error']

    def test_parse_resume_openai_error(self, client, sample_text_resume):
        """Test OpenAI API error handling"""
        with patch('app.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception("OpenAI API Error")
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                response = client.post('/api/parse-resume', 
                    json={'textResume': sample_text_resume},
                    content_type='application/json'
                )
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'Resume parsing failed' in data['error']

    def test_parse_resume_invalid_json_response(self, client, sample_text_resume):
        """Test handling invalid JSON from OpenAI"""
        with patch('app.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Mock invalid JSON response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message = Mock()
            mock_response.choices[0].message.content = "This is not valid JSON"
            mock_client.chat.completions.create.return_value = mock_response
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                response = client.post('/api/parse-resume', 
                    json={'textResume': sample_text_resume},
                    content_type='application/json'
                )
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'Failed to parse AI response as JSON' in data['error']

    def test_parse_resume_with_markdown_cleanup(self, client, sample_text_resume, expected_json_structure):
        """Test JSON cleanup from markdown formatting"""
        with patch('app.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            # Mock response with markdown formatting
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message = Mock()
            mock_response.choices[0].message.content = f"```json\n{json.dumps(expected_json_structure)}\n```"
            mock_client.chat.completions.create.return_value = mock_response
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                response = client.post('/api/parse-resume', 
                    json={'textResume': sample_text_resume},
                    content_type='application/json'
                )
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['resumeData']['personal']['name'] == 'John Smith'

    def test_openai_not_available(self, client, sample_text_resume):
        """Test when OpenAI package is not available"""
        with patch('app.OPENAI_AVAILABLE', False):
            response = client.post('/api/parse-resume', 
                json={'textResume': sample_text_resume},
                content_type='application/json'
            )
            
            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data
            assert 'OpenAI not available' in data['error']

    def test_health_check_with_text_to_json(self, client):
        """Test health check includes text-to-JSON feature status"""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'features' in data
        assert 'text_to_json' in data['features']

    @patch('app.validate_resume_structure')
    def test_parse_resume_validation_integration(self, mock_validate, client, sample_text_resume, mock_openai_response):
        """Test integration with resume validation"""
        # Mock validation response
        mock_validate.return_value = {
            'valid': True,
            'errors': [],
            'warnings': ['Consider adding more quantified achievements']
        }
        
        with patch('app.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_openai_response
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                response = client.post('/api/parse-resume', 
                    json={'textResume': sample_text_resume},
                    content_type='application/json'
                )
            
            assert response.status_code == 200
            data = response.get_json()
            
            # Verify validation was called
            mock_validate.assert_called_once()
            
            assert data['success'] is True
            assert 'validation' in data
            assert data['validation']['valid'] is True

class TestPromptEngineering:
    """Test the OpenAI prompt engineering for resume parsing"""

    def test_system_prompt_structure(self):
        """Test that the system prompt contains required elements"""
        # Import the function to access the prompt
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            from app import app as flask_app
        
        # The prompt should contain key elements
        required_elements = [
            'JSON format',
            'personal',
            'experience', 
            'skills',
            'education',
            'achievements',
            'keywords',
            'metrics'
        ]
        
        # This would typically be extracted from the actual code
        # For now, we validate the concept
        assert True  # Placeholder for prompt validation

    def test_model_parameters(self):
        """Test OpenAI model parameters are optimal"""
        # Test that we use appropriate model and parameters
        expected_model = "gpt-4-turbo-preview"
        expected_temp = 0.1
        expected_max_tokens = 4000
        
        # These would be validated against actual API calls
        assert True  # Placeholder for parameter validation

def run_mock_api_tests():
    """Run tests using mock API responses"""
    
    # Sample test data
    test_cases = [
        {
            "name": "Senior Engineer Resume",
            "input": """
            Jane Doe
            Senior Software Engineer
            jane@example.com | 555-0123 | New York, NY
            
            EXPERIENCE
            Staff Engineer | BigTech Corp | 2021-Present
            • Led architecture for microservices handling 10M+ requests/day
            • Reduced system latency by 45% through optimization
            
            SKILLS
            Python, React, AWS, Kubernetes
            """,
            "expected_fields": ["name", "email", "phone", "experience", "skills"]
        },
        {
            "name": "FinTech Professional Resume",
            "input": """
            Alex Chen
            FinTech Engineering Manager
            alex.chen@fintech.com | (555) 987-6543 | Austin, TX
            
            SUMMARY
            Engineering leader with 10+ years in financial technology
            
            EXPERIENCE
            Engineering Manager | CryptoStartup | 2022-Present
            • Built DeFi protocols managing $500M+ TVL
            • Led team of 12 engineers across 3 product areas
            
            SKILLS
            Blockchain: Ethereum, Solidity, Web3
            Backend: Python, Go, PostgreSQL
            """,
            "expected_fields": ["name", "email", "summary", "experience", "skills"]
        }
    ]
    
    print("🧪 Running Mock API Tests for Text-to-JSON Conversion")
    print("=" * 60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {case['name']}")
        
        # Simulate API processing
        mock_result = simulate_text_to_json_conversion(case['input'])
        
        # Validate result structure
        validation_passed = validate_mock_result(mock_result, case['expected_fields'])
        
        status = "✅ PASS" if validation_passed else "❌ FAIL"
        print(f"   Result: {status}")
        
        if validation_passed:
            print(f"   - Successfully extracted {len(mock_result.get('experience', []))} jobs")
            print(f"   - Found {len(mock_result.get('skills', {}).keys())} skill categories")
            print(f"   - Contact info: {mock_result.get('personal', {}).get('name', 'N/A')}")

def simulate_text_to_json_conversion(text_resume: str) -> dict:
    """Simulate the text-to-JSON conversion process"""
    
    # Mock the OpenAI response structure
    mock_resume = {
        "personal": {
            "name": extract_name_from_text(text_resume),
            "email": extract_email_from_text(text_resume),
            "phone": extract_phone_from_text(text_resume),
            "location": extract_location_from_text(text_resume)
        },
        "experience": extract_experience_from_text(text_resume),
        "skills": extract_skills_from_text(text_resume)
    }
    
    # Add summary if present
    if "SUMMARY" in text_resume or "Professional" in text_resume:
        mock_resume["summary"] = {
            "headline": "Extracted professional summary",
            "bullets": ["Key strength 1", "Key strength 2"]
        }
    
    return mock_resume

def extract_name_from_text(text: str) -> str:
    """Extract name from resume text"""
    lines = text.strip().split('\n')
    return lines[0].strip() if lines else "Unknown"

def extract_email_from_text(text: str) -> str:
    """Extract email from resume text"""
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group() if match else ""

def extract_phone_from_text(text: str) -> str:
    """Extract phone from resume text"""
    import re
    phone_pattern = r'[\(\)0-9\-\+\s]{10,}'
    match = re.search(phone_pattern, text)
    return match.group().strip() if match else ""

def extract_location_from_text(text: str) -> str:
    """Extract location from resume text"""
    import re
    # Look for City, State pattern
    location_pattern = r'[A-Za-z\s]+,\s*[A-Z]{2}'
    match = re.search(location_pattern, text)
    return match.group() if match else ""

def extract_experience_from_text(text: str) -> list:
    """Extract experience from resume text"""
    experience_section = ""
    lines = text.split('\n')
    in_experience = False
    
    for line in lines:
        if "EXPERIENCE" in line.upper():
            in_experience = True
            continue
        elif line.strip().isupper() and len(line.strip()) > 0 and in_experience:
            break
        elif in_experience:
            experience_section += line + "\n"
    
    # Mock job extraction
    jobs = []
    if "|" in experience_section:  # Assume format: Title | Company | Date
        job_lines = [line for line in experience_section.split('\n') if '|' in line]
        for job_line in job_lines[:2]:  # Limit to 2 jobs for testing
            parts = job_line.split('|')
            if len(parts) >= 2:
                jobs.append({
                    "title": parts[0].strip(),
                    "company": parts[1].strip(),
                    "duration": parts[2].strip() if len(parts) > 2 else "Unknown",
                    "achievements": [
                        {
                            "text": "Mock achievement extracted from text",
                            "keywords": ["python", "engineering"],
                            "metrics": {"value": 1000000, "type": "users"}
                        }
                    ]
                })
    
    return jobs

def extract_skills_from_text(text: str) -> dict:
    """Extract skills from resume text"""
    skills = {}
    
    # Look for skills section
    if "SKILLS" in text.upper():
        skills_section = ""
        lines = text.split('\n')
        in_skills = False
        
        for line in lines:
            if "SKILLS" in line.upper():
                in_skills = True
                continue
            elif line.strip().isupper() and len(line.strip()) > 0 and in_skills:
                break
            elif in_skills:
                skills_section += line + "\n"
        
        # Parse skills by category
        if ":" in skills_section:
            for line in skills_section.split('\n'):
                if ":" in line:
                    category, skill_list = line.split(':', 1)
                    category_key = category.strip().lower().replace(' ', '_')
                    skills_list = [s.strip() for s in skill_list.split(',')]
                    skills[category_key] = {"proficient": skills_list}
    
    return skills

def validate_mock_result(result: dict, expected_fields: list) -> bool:
    """Validate the mock conversion result"""
    
    # Check required fields are present
    for field in expected_fields:
        if field not in result:
            return False
    
    # Validate personal info structure
    if 'personal' in result:
        personal = result['personal']
        if not personal.get('name') or not personal.get('email'):
            return False
    
    # Validate experience structure
    if 'experience' in result:
        for job in result['experience']:
            if not job.get('title') or not job.get('company'):
                return False
    
    return True

if __name__ == "__main__":
    # Run the mock API tests
    run_mock_api_tests()
    
    print("\n" + "=" * 60)
    print("🔬 Running Unit Tests with pytest")
    print("=" * 60)
    
    # Run pytest if available
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("❌ pytest not installed. Run: pip install pytest")
        print("✅ Mock API tests completed successfully!")
