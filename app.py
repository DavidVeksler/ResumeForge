#!/usr/bin/env python3
"""
Flask Backend API for Resume Optimizer
Provides endpoints for resume optimization and ATS scoring
"""

try:
    from flask import Flask, request, jsonify, send_file
    from flask_cors import CORS
    import pdfkit
    FLASK_AVAILABLE = True
    PDFKIT_AVAILABLE = True
except ImportError as e:
    if 'pdfkit' in str(e):
        print("pdfkit not installed. PDF export will be disabled.")
        PDFKIT_AVAILABLE = False
        from flask import Flask, request, jsonify, send_file
        from flask_cors import CORS
        FLASK_AVAILABLE = True
    else:
        print("Flask not installed. Please install with: pip install Flask Flask-CORS")
        FLASK_AVAILABLE = False
        PDFKIT_AVAILABLE = False
        Flask = None
        CORS = None

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("OpenAI not installed. Text-to-JSON conversion will be disabled.")
    OPENAI_AVAILABLE = False
    OpenAI = None

import json
import os
import tempfile
from resume_generator import ResumeGenerator, extract_keywords_from_job_description
from typing import Dict, List, Any
import re

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed, using system environment variables")

if FLASK_AVAILABLE:
    app = Flask(__name__)
    CORS(app)  # Enable CORS for React frontend

if FLASK_AVAILABLE:
    @app.route('/api/optimize', methods=['POST'])
    def optimize_resume():
        """
        Optimize resume based on job description
        Expected payload: {
            "resumeData": {...},
            "jobDescription": "..."
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'resumeData' not in data or 'jobDescription' not in data:
                return jsonify({'error': 'Missing resumeData or jobDescription'}), 400
            
            resume_data = data['resumeData']
            job_description = data['jobDescription']
            
            # Validate inputs
            resume_validation = validate_resume_structure(resume_data)
            if not resume_validation['valid']:
                return jsonify({
                    'error': 'Invalid resume format',
                    'validation_errors': resume_validation['errors']
                }), 400
            
            job_validation = validate_job_description(job_description)
            if not job_validation['valid']:
                return jsonify({
                    'error': 'Invalid job description',
                    'validation_errors': job_validation['errors']
                }), 400
            
            # Create resume generator
            generator = ResumeGenerator(resume_data)
            
            # Extract keywords from job description
            role_keywords = extract_keywords_from_job_description(job_description)
            
            # Generate default resume
            default_html = generator.generate_ats_template()
            default_score = calculate_ats_score(resume_data, role_keywords)
            
            # Customize for role and generate optimized resume
            customized_data = generator.customize_for_role(job_description, role_keywords)
            optimized_generator = ResumeGenerator(customized_data)
            optimized_html = optimized_generator.generate_ats_template()
            optimized_score = calculate_ats_score(customized_data, role_keywords)
            
            # Generate optimization summary
            optimizations = generate_optimization_summary(resume_data, customized_data, role_keywords)
            
            return jsonify({
                'success': True,
                'defaultHtml': default_html,
                'optimizedHtml': optimized_html,
                'defaultScore': default_score,
                'optimizedScore': optimized_score,
                'improvement': optimized_score - default_score,
                'optimizations': optimizations,
                'keywords': role_keywords[:20]  # Top 20 keywords
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/export-pdf', methods=['POST'])
    def export_pdf():
        """Export resume as PDF"""
        if not PDFKIT_AVAILABLE:
            return jsonify({'error': 'PDF export not available. Install wkhtmltopdf and pdfkit.'}), 500
        
        try:
            data = request.get_json()
            if not data or 'html' not in data:
                return jsonify({'error': 'Missing HTML content'}), 400
            
            html_content = data['html']
            filename = data.get('filename', 'resume.pdf')
            
            # Configure PDF options
            options = {
                'page-size': 'Letter',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                pdf_path = tmp_file.name
            
            # Generate PDF
            pdfkit.from_string(html_content, pdf_path, options=options)
            
            return send_file(pdf_path, as_attachment=True, download_name=filename, mimetype='application/pdf')
            
        except Exception as e:
            return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

    @app.route('/api/validate-resume', methods=['POST'])
    def validate_resume():
        """Validate resume JSON structure"""
        try:
            data = request.get_json()
            if not data or 'resumeData' not in data:
                return jsonify({'error': 'Missing resumeData'}), 400
            
            resume_data = data['resumeData']
            validation_result = validate_resume_structure(resume_data)
            
            return jsonify(validation_result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/sample-resume', methods=['GET'])
    def get_sample_resume():
        """Get sample resume template"""
        try:
            # Load the existing resume as a template
            with open('david_resume_json.json', 'r') as f:
                sample_data = json.load(f)
            
            # Anonymize the sample data
            sample_data['personal'] = {
                "name": "Your Full Name",
                "email": "your.email@example.com",
                "phone": "+1 (555) 123-4567",
                "location": "Your City, State",
                "linkedin": "linkedin.com/in/yourprofile"
            }
            
            return jsonify({
                'success': True,
                'sampleData': sample_data,
                'instructions': {
                    'personal': 'Required: Your contact information',
                    'summary': 'Professional summary with headline and bullet points',
                    'experience': 'Work history with achievements containing keywords and metrics',
                    'skills': 'Technical skills organized by category and proficiency level',
                    'education': 'Educational background',
                    'projects': 'Key projects with descriptions and keywords'
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/parse-resume', methods=['POST'])
    def parse_text_resume():
        """Convert text resume to structured JSON using configurable AI provider"""
        if not OPENAI_AVAILABLE:
            return jsonify({'error': 'OpenAI package not available. Install openai package.'}), 500
        
        try:
            data = request.get_json()
            if not data or 'textResume' not in data:
                return jsonify({'error': 'Missing textResume field'}), 400
            
            text_resume = data['textResume'].strip()
            if not text_resume:
                return jsonify({'error': 'Text resume cannot be empty'}), 400
            
            # Get AI provider configuration
            ai_provider = os.getenv('AI_PROVIDER', 'local').lower()
            
            # Initialize client based on provider
            if ai_provider == 'openai':
                # OpenAI API configuration
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    return jsonify({'error': 'OpenAI API key not configured. Set OPENAI_API_KEY environment variable.'}), 500
                
                client = OpenAI(api_key=api_key)
                model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
                
            else:
                # Local LLM configuration (default)
                base_url = os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1')
                client = OpenAI(
                    api_key="local-key",  # Local LLM doesn't require real API key
                    base_url=base_url
                )
                model_name = os.getenv('LOCAL_MODEL_NAME', 'local-model')
            
            # Create the parsing prompt
            system_prompt = """You are a resume parsing expert. Convert the provided text resume into a structured JSON format exactly matching this schema:

{
  "personal": {
    "name": "Full Name",
    "email": "email@example.com", 
    "phone": "+1 (555) 123-4567",
    "location": "City, State",
    "linkedin": "linkedin.com/in/profile"
  },
  "summary": {
    "headline": "Professional headline/summary",
    "bullets": ["Key strength 1", "Key strength 2", "Key strength 3"]
  },
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State", 
      "duration": "Start Date - End Date",
      "description": "Brief role description",
      "achievements": [
        {
          "text": "Achievement description with specific metrics",
          "keywords": ["relevant", "keywords", "for", "ats"],
          "metrics": {"value": 100000, "type": "revenue_impact"}
        }
      ]
    }
  ],
  "skills": {
    "programming_languages": {
      "expert": ["Language1", "Language2"],
      "proficient": ["Language3", "Language4"], 
      "familiar": ["Language5"]
    },
    "web_technologies": {
      "expert": ["Framework1"],
      "proficient": ["Framework2", "Framework3"]
    },
    "fintech": ["blockchain", "defi", "payments"],
    "leadership": ["team management", "project leadership"]
  },
  "education": [
    {
      "degree": "Degree Name",
      "school": "University Name",
      "duration": "Start - End Year",
      "description": "Relevant details or achievements"
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "description": "Project description highlighting impact",
      "keywords": ["relevant", "technical", "keywords"],
      "achievements": ["Key outcome 1", "Key outcome 2"]
    }
  ]
}

Instructions:
1. Extract ALL information accurately from the text
2. For achievements, identify quantifiable metrics and convert to numbers
3. Add relevant ATS keywords based on the role/industry context
4. Organize skills by proficiency level and category
5. If information is missing, use reasonable defaults or omit optional fields
6. Ensure all JSON is valid and properly formatted
7. Focus on FinTech/technology keywords when applicable

Return ONLY the JSON structure, no additional text."""

            # Make API call to configured AI provider
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Convert this resume to JSON:\n\n{text_resume}"}
                ],
                temperature=0.1,  # Low temperature for consistent formatting
                max_tokens=4000
            )
            
            # Parse the response
            json_content = response.choices[0].message.content.strip()
            
            # Clean up the response (remove any markdown formatting)
            if json_content.startswith('```json'):
                json_content = json_content[7:]
            if json_content.endswith('```'):
                json_content = json_content[:-3]
            
            # Parse and validate the JSON
            try:
                parsed_resume = json.loads(json_content)
            except json.JSONDecodeError as e:
                return jsonify({
                    'error': 'Failed to parse AI response as JSON',
                    'details': str(e),
                    'raw_response': json_content[:500]  # First 500 chars for debugging
                }), 500
            
            # Validate the parsed resume structure
            validation_result = validate_resume_structure(parsed_resume)
            
            return jsonify({
                'success': True,
                'resumeData': parsed_resume,
                'validation': validation_result,
                'message': 'Resume successfully converted to structured JSON format'
            })
            
        except Exception as e:
            return jsonify({'error': f'Resume parsing failed: {str(e)}'}), 500

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Enhanced health check endpoint with detailed system information"""
        import datetime
        import subprocess
        import platform
        
        # Try to import psutil, but handle gracefully if not available
        try:
            import psutil
            PSUTIL_AVAILABLE = True
        except ImportError:
            PSUTIL_AVAILABLE = False
            psutil = None
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'version': '1.0.0',
            'message': 'Resume Optimizer API is running'
        }
        
        # System Information
        system_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version()
        }
        
        if PSUTIL_AVAILABLE:
            try:
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                system_info.update({
                    'memory': {
                        'total_gb': round(memory.total / (1024**3), 2),
                        'available_gb': round(memory.available / (1024**3), 2),
                        'used_percent': memory.percent
                    },
                    'disk': {
                        'total_gb': round(disk.total / (1024**3), 2),
                        'free_gb': round(disk.free / (1024**3), 2),
                        'used_percent': round((disk.used / disk.total) * 100, 1)
                    }
                })
            except Exception as e:
                system_info['psutil_error'] = f'Could not retrieve detailed system info: {str(e)}'
        else:
            system_info['note'] = 'Install psutil for detailed memory and disk usage information'
        
        health_data['system'] = system_info
        
        # Dependency Checks
        dependencies = {
            'flask': FLASK_AVAILABLE,
            'openai': OPENAI_AVAILABLE,
            'pdfkit': PDFKIT_AVAILABLE,
            'wkhtmltopdf': False,
            'psutil': PSUTIL_AVAILABLE,
            'dotenv': False
        }
        
        # Check wkhtmltopdf binary
        try:
            result = subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, check=True, timeout=5)
            dependencies['wkhtmltopdf'] = True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # Try alternative paths
            try:
                result = subprocess.run(['/usr/bin/wkhtmltopdf', '--version'], capture_output=True, check=True, timeout=5)
                dependencies['wkhtmltopdf'] = True
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                try:
                    result = subprocess.run(['/usr/local/bin/wkhtmltopdf', '--version'], capture_output=True, check=True, timeout=5)
                    dependencies['wkhtmltopdf'] = True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    dependencies['wkhtmltopdf'] = False
            
        # Check python-dotenv
        try:
            import dotenv
            dependencies['dotenv'] = True
        except ImportError:
            dependencies['dotenv'] = False
        
        health_data['dependencies'] = dependencies
        
        # File System Checks
        file_checks = {}
        critical_files = [
            'david_resume_json.json',
            'resume_generator.py',
            '.env'
        ]
        
        for file_path in critical_files:
            try:
                if os.path.exists(file_path):
                    stat_info = os.stat(file_path)
                    file_checks[file_path] = {
                        'exists': True,
                        'readable': os.access(file_path, os.R_OK),
                        'size_bytes': stat_info.st_size,
                        'last_modified': datetime.datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                    }
                else:
                    file_checks[file_path] = {'exists': False}
            except Exception as e:
                file_checks[file_path] = {'error': str(e)}
        
        health_data['files'] = file_checks
        
        # Environment Configuration
        env_config = {
            'AI_PROVIDER': os.getenv('AI_PROVIDER', 'local'),
            'OPENAI_MODEL': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            'OPENAI_API_KEY_SET': bool(os.getenv('OPENAI_API_KEY')),
            'LOCAL_LLM_BASE_URL': os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1'),
            'LOCAL_MODEL_NAME': os.getenv('LOCAL_MODEL_NAME', 'local-model'),
            'FLASK_ENV': os.getenv('FLASK_ENV', 'production')
        }
        
        health_data['environment'] = env_config
        
        # AI Provider Configuration and Connectivity
        ai_provider = os.getenv('AI_PROVIDER', 'local').lower()
        ai_status = {
            'provider': ai_provider,
            'configured': False,
            'connectivity_test': False
        }
        
        if ai_provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            ai_status.update({
                'model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                'configured': bool(api_key),
                'api_key_configured': bool(api_key)
            })
            
            # Test OpenAI connectivity (optional, can be slow)
            if api_key and OPENAI_AVAILABLE:
                try:
                    client = OpenAI(api_key=api_key)
                    # Quick test call with minimal usage
                    response = client.chat.completions.create(
                        model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                        messages=[{"role": "user", "content": "test"}],
                        max_tokens=1
                    )
                    ai_status['connectivity_test'] = True
                    ai_status['last_test'] = datetime.datetime.utcnow().isoformat() + 'Z'
                except Exception as e:
                    ai_status['connectivity_test'] = False
                    ai_status['connectivity_error'] = str(e)
        else:
            base_url = os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1')
            model_name = os.getenv('LOCAL_MODEL_NAME', 'local-model')
            ai_status.update({
                'base_url': base_url,
                'model': model_name,
                'configured': True  # Local LLM doesn't require API key
            })
            
            # Test local LLM connectivity
            if OPENAI_AVAILABLE:
                try:
                    client = OpenAI(api_key="local-key", base_url=base_url)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": "test"}],
                        max_tokens=1
                    )
                    ai_status['connectivity_test'] = True
                    ai_status['last_test'] = datetime.datetime.utcnow().isoformat() + 'Z'
                except Exception as e:
                    ai_status['connectivity_test'] = False
                    ai_status['connectivity_error'] = str(e)
        
        health_data['ai_provider'] = ai_status
        
        # Feature Availability
        features = {
            'resume_optimization': FLASK_AVAILABLE,
            'pdf_export': PDFKIT_AVAILABLE and dependencies['wkhtmltopdf'],
            'text_to_json_parsing': OPENAI_AVAILABLE and ai_status['configured'],
            'resume_validation': True,
            'sample_template': file_checks.get('david_resume_json.json', {}).get('exists', False),
            'keyword_extraction': True,
            'ats_scoring': True
        }
        
        health_data['features'] = features
        
        # Overall Health Assessment
        critical_issues = []
        warnings = []
        
        # Check for critical issues
        if not FLASK_AVAILABLE:
            critical_issues.append('Flask framework not available')
        
        if not file_checks.get('resume_generator.py', {}).get('exists'):
            critical_issues.append('Core resume generator module missing')
        
        if not ai_status['configured']:
            critical_issues.append('AI provider not properly configured')
        
        # Check for warnings
        if not dependencies['wkhtmltopdf']:
            warnings.append('wkhtmltopdf not available - PDF export disabled')
        
        if not PSUTIL_AVAILABLE:
            warnings.append('psutil not available - system monitoring limited')
        
        if ai_provider == 'openai' and not ai_status.get('connectivity_test'):
            warnings.append('OpenAI API connectivity could not be verified')
        
        if ai_provider == 'local' and not ai_status.get('connectivity_test'):
            warnings.append('Local LLM connectivity could not be verified')
        
        # Set overall status
        if critical_issues:
            health_data['status'] = 'unhealthy'
            health_data['message'] = 'Critical issues detected'
        elif warnings:
            health_data['status'] = 'warning'
            health_data['message'] = 'Service operational with warnings'
        else:
            health_data['status'] = 'healthy'
            health_data['message'] = 'All systems operational'
        
        health_data['issues'] = {
            'critical': critical_issues,
            'warnings': warnings
        }
        
        return jsonify(health_data)

def calculate_ats_score(resume_data: Dict[str, Any], role_keywords: List[str]) -> int:
    """
    Calculate ATS score based on keyword matches and resume structure
    Returns score from 0-100
    """
    total_score = 0
    max_score = 100
    
    # Keyword matching (40 points max)
    resume_text = extract_resume_text(resume_data).lower()
    matched_keywords = 0
    
    for keyword in role_keywords[:20]:  # Check top 20 keywords
        if keyword.lower() in resume_text:
            matched_keywords += 1
    
    keyword_score = min(40, (matched_keywords / 20) * 40)
    total_score += keyword_score
    
    # Skills section presence (15 points)
    if 'skills' in resume_data and resume_data['skills']:
        total_score += 15
    
    # Experience section with achievements (20 points)
    if 'experience' in resume_data:
        achievement_count = sum(len(job.get('achievements', [])) for job in resume_data['experience'])
        achievement_score = min(20, (achievement_count / 10) * 20)
        total_score += achievement_score
    
    # Contact information completeness (10 points)
    contact_fields = ['name', 'email', 'phone', 'location']
    if 'personal' in resume_data:
        contact_score = sum(5 if field in resume_data['personal'] else 0 for field in contact_fields[:2])
        contact_score += sum(2.5 if field in resume_data['personal'] else 0 for field in contact_fields[2:])
        total_score += contact_score
    
    # Professional summary (10 points)
    if 'summary' in resume_data and resume_data['summary'].get('headline'):
        total_score += 10
    
    # Education section (5 points)
    if 'education' in resume_data and resume_data['education']:
        total_score += 5
    
    return min(100, int(total_score))

def extract_resume_text(resume_data: Dict[str, Any]) -> str:
    """Extract all text content from resume data for keyword matching"""
    text_parts = []
    
    # Personal info
    if 'personal' in resume_data:
        text_parts.extend(resume_data['personal'].values())
    
    # Summary
    if 'summary' in resume_data:
        if 'headline' in resume_data['summary']:
            text_parts.append(resume_data['summary']['headline'])
        if 'bullets' in resume_data['summary']:
            text_parts.extend(resume_data['summary']['bullets'])
    
    # Experience
    if 'experience' in resume_data:
        for job in resume_data['experience']:
            text_parts.extend([job.get('title', ''), job.get('company', ''), job.get('description', '')])
            for achievement in job.get('achievements', []):
                text_parts.append(achievement.get('text', ''))
                text_parts.extend(achievement.get('keywords', []))
    
    # Skills
    if 'skills' in resume_data:
        for category in resume_data['skills'].values():
            if isinstance(category, dict):
                for skill_level in category.values():
                    if isinstance(skill_level, list):
                        text_parts.extend(skill_level)
            elif isinstance(category, list):
                text_parts.extend(category)
    
    # Education
    if 'education' in resume_data:
        for edu in resume_data['education']:
            text_parts.extend([edu.get('degree', ''), edu.get('school', ''), edu.get('description', '')])
    
    # Projects
    if 'projects' in resume_data:
        for project in resume_data['projects']:
            text_parts.extend([project.get('name', ''), project.get('description', '')])
            text_parts.extend(project.get('keywords', []))
    
    return ' '.join(str(part) for part in text_parts if part)

def generate_optimization_summary(original_data: Dict, optimized_data: Dict, role_keywords: List[str]) -> List[Dict]:
    """Generate summary of optimizations applied"""
    optimizations = []
    
    # Keywords added
    keyword_count = len(role_keywords[:15])
    key_keywords = ', '.join([f'"{kw}"' for kw in role_keywords[:3]])
    optimizations.append({
        'icon': 'bi-key-fill',
        'iconClass': 'optimizations-icon-key',
        'text': f'Added <strong>{keyword_count} keywords</strong> from job description, including {key_keywords}.'
    })
    
    # Achievement reordering
    for job in optimized_data.get('experience', []):
        if any(achievement.get('relevance_score', 0) > 0 for achievement in job.get('achievements', [])):
            optimizations.append({
                'icon': 'bi-arrow-up-down',
                'iconClass': 'optimizations-icon-reorder',
                'text': f'<strong>Reordered achievements</strong> under "{job["title"]}" role to prioritize relevant experience.'
            })
            break
    
    # Metrics highlighting
    metric_count = 0
    for job in original_data.get('experience', []):
        for achievement in job.get('achievements', []):
            if achievement.get('metrics'):
                metric_count += 1
    
    if metric_count > 0:
        optimizations.append({
            'icon': 'bi-graph-up-arrow',
            'iconClass': 'optimizations-icon-metrics',
            'text': f'Highlighted <strong>key metrics</strong> like "$100M TVL" and quantified achievements for impact.'
        })
    
    # Skills enhancement
    optimizations.append({
        'icon': 'bi-pencil-square',
        'iconClass': 'optimizations-icon-skills',
        'text': 'Enhanced "Technical Skills" to better reflect <strong>FinTech and technical</strong> expertise.'
    })
    
    # Summary update
    optimizations.append({
        'icon': 'bi-file-earmark-text-fill',
        'iconClass': 'optimizations-icon-summary',
        'text': 'Updated professional summary for stronger alignment with role requirements.'
    })
    
    return optimizations

def validate_resume_structure(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate resume JSON structure and provide detailed feedback"""
    errors = []
    warnings = []
    
    # Required fields validation
    if not isinstance(resume_data, dict):
        return {'valid': False, 'errors': ['Resume data must be a JSON object'], 'warnings': []}
    
    # Personal information validation
    if 'personal' not in resume_data:
        errors.append('Missing required "personal" section')
    else:
        personal = resume_data['personal']
        required_personal = ['name', 'email']
        for field in required_personal:
            if field not in personal or not personal[field]:
                errors.append(f'Missing required personal.{field}')
        
        # Email validation
        if 'email' in personal and personal['email']:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, personal['email']):
                errors.append('Invalid email format in personal.email')
    
    # Experience validation
    if 'experience' not in resume_data:
        warnings.append('Missing "experience" section - recommended for ATS optimization')
    else:
        experience = resume_data['experience']
        if not isinstance(experience, list):
            errors.append('"experience" must be an array of job objects')
        else:
            for i, job in enumerate(experience):
                if not isinstance(job, dict):
                    errors.append(f'Experience item {i+1} must be an object')
                    continue
                
                required_job_fields = ['title', 'company', 'duration']
                for field in required_job_fields:
                    if field not in job or not job[field]:
                        warnings.append(f'Experience item {i+1} missing recommended field: {field}')
                
                if 'achievements' in job:
                    achievements = job['achievements']
                    if not isinstance(achievements, list):
                        errors.append(f'Experience item {i+1} achievements must be an array')
                    else:
                        for j, achievement in enumerate(achievements):
                            if not isinstance(achievement, dict) or 'text' not in achievement:
                                errors.append(f'Achievement {j+1} in job {i+1} must have "text" field')
    
    # Skills validation
    if 'skills' not in resume_data:
        warnings.append('Missing "skills" section - important for ATS scoring')
    
    # Summary validation
    if 'summary' not in resume_data:
        warnings.append('Missing "summary" section - helps with ATS optimization')
    else:
        summary = resume_data['summary']
        if 'headline' not in summary or not summary['headline']:
            warnings.append('Missing summary headline - recommended for professional impact')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'recommendations': [
            'Include quantifiable achievements with metrics (e.g., "$100M TVL", "20+ engineers")',
            'Add relevant keywords to each achievement for better ATS matching',
            'Organize skills by proficiency level (expert, proficient, familiar)',
            'Include education section for complete professional profile'
        ] if len(errors) == 0 else []
    }

def validate_job_description(job_description: str) -> Dict[str, Any]:
    """Validate job description input"""
    errors = []
    warnings = []
    
    if not job_description or not job_description.strip():
        errors.append('Job description cannot be empty')
        return {'valid': False, 'errors': errors, 'warnings': warnings}
    
    # Length validation
    word_count = len(job_description.split())
    if word_count < 50:
        warnings.append(f'Job description is quite short ({word_count} words). Longer descriptions provide better optimization.')
    elif word_count > 2000:
        warnings.append(f'Job description is very long ({word_count} words). Consider focusing on key requirements.')
    
    # Content validation
    common_sections = ['requirements', 'responsibilities', 'qualifications', 'skills', 'experience']
    found_sections = sum(1 for section in common_sections if section.lower() in job_description.lower())
    
    if found_sections < 2:
        warnings.append('Job description may be missing key sections (requirements, responsibilities, qualifications)')
    
    # Technical terms check
    technical_indicators = ['years', 'experience', 'required', 'preferred', 'must have', 'should have']
    found_indicators = sum(1 for indicator in technical_indicators if indicator.lower() in job_description.lower())
    
    if found_indicators < 2:
        warnings.append('Job description may lack specific requirements for better keyword extraction')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'word_count': word_count,
        'estimated_keywords': min(60, word_count // 10)  # Rough estimate
    }

if __name__ == '__main__':
    if not FLASK_AVAILABLE:
        print("Error: Flask is not installed.")
        print("Please install Flask with: pip install Flask Flask-CORS python-dotenv")
        exit(1)
    
    print("Starting Resume Optimizer API server...")
    app.run(debug=True, port=5000, host='127.0.0.1')