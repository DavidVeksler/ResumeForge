#!/usr/bin/env python3
"""
Flask Backend API for Resume Optimizer
Refactored version with proper service layer architecture
"""

# Dependency imports with graceful error handling
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

import json
import os
import tempfile
from typing import Any, Dict

# OpenAI import for patching/testing
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed, using system environment variables")

# Import refactored services
from services.ai_service import AIService, AIProviderError, OPENAI_AVAILABLE
from services.resume_service import ResumeService
from services.scoring_service import ScoringService
from validation.validators import ResumeValidator, JobDescriptionValidator

# Initialize Flask app
if FLASK_AVAILABLE:
    app = Flask(__name__)
    CORS(app)


def validate_resume_structure(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate resume data and return a serializable result."""
    validation = ResumeValidator.validate(resume_data)
    return validation.to_dict()


def _strip_json_content(content: str) -> str:
    """Remove optional markdown fences from AI responses."""
    cleaned = content.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


# =============================================================================
# API ENDPOINTS
# =============================================================================

if FLASK_AVAILABLE:

    @app.route('/api/optimize', methods=['POST'])
    def optimize_resume():
        """Optimize resume based on job description"""
        try:
            data = request.get_json()

            if not data or 'resumeData' not in data or 'jobDescription' not in data:
                return jsonify({'error': 'Missing resumeData or jobDescription'}), 400

            resume_data = data['resumeData']
            job_description = data['jobDescription']

            # Validate inputs
            resume_validation = ResumeValidator.validate(resume_data)
            if not resume_validation.is_valid:
                return jsonify({
                    'error': 'Invalid resume format',
                    'validation_errors': resume_validation.to_dict()
                }), 400

            job_validation = JobDescriptionValidator.validate(job_description)
            if not job_validation['valid']:
                return jsonify({
                    'error': 'Invalid job description',
                    'validation_errors': job_validation
                }), 400

            # Optimize resume using service layer
            default_html, optimized_html, customized_data, role_keywords = \
                ResumeService.optimize_resume(resume_data, job_description)

            # Calculate ATS scores
            default_score = ScoringService.calculate_ats_score(resume_data, role_keywords)
            optimized_score = ScoringService.calculate_ats_score(customized_data, role_keywords)

            # Generate optimization summary
            optimizations = ScoringService.generate_optimization_summary(
                resume_data,
                customized_data,
                role_keywords
            )

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
            return jsonify({
                'error': 'PDF export not available. Install wkhtmltopdf and pdfkit.'
            }), 500

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

            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/pdf'
            )

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
            validation_result = ResumeValidator.validate(resume_data)

            return jsonify(validation_result.to_dict())

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
        if not OPENAI_AVAILABLE or OpenAI is None:
            return jsonify({
                'error': 'OpenAI not available. Install openai package.'
            }), 500

        data = request.get_json()
        if not data or 'textResume' not in data:
            return jsonify({'error': 'Missing textResume field'}), 400

        text_resume = data.get('textResume', '')
        if not text_resume or not str(text_resume).strip():
            return jsonify({'error': 'Text resume cannot be empty'}), 400

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500

        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=[
                    {"role": "system", "content": AIService.get_parsing_system_prompt()},
                    {"role": "user", "content": f"Convert this resume to JSON:\n\n{text_resume.strip()}"}
                ],
                temperature=0.1,
                max_tokens=4000
            )

            json_content = _strip_json_content(response.choices[0].message.content)
            parsed_resume = json.loads(json_content)

        except json.JSONDecodeError as e:
            return jsonify({'error': f'Failed to parse AI response as JSON: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'error': f'Resume parsing failed: {str(e)}'}), 500

        validation_result = validate_resume_structure(parsed_resume)

        return jsonify({
            'success': True,
            'resumeData': parsed_resume,
            'validation': validation_result,
            'message': 'Resume successfully converted to structured JSON format'
        })

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Enhanced health check endpoint with detailed system information"""
        from routes.health_routes import get_health_status
        return jsonify(get_health_status())


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    if not FLASK_AVAILABLE:
        print("Error: Flask is not installed.")
        print("Please install Flask with: pip install Flask Flask-CORS python-dotenv")
        exit(1)

    print("Starting Resume Optimizer API server...")
    app.run(debug=True, port=5000, host='127.0.0.1')
