"""
Consolidated API Routes
Merges all endpoints from app.py, run_app.py, and simple_server.py
"""

import json
import os
import tempfile
from datetime import datetime
from typing import Optional

from .. import __version__

try:
    from flask import Flask, request, jsonify, send_file, after_this_request
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None
    CORS = None

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False

from .. import __version__
from ..services import (
    ResumeService,
    ScoringService,
    ParsingService,
    ValidationService,
)
from ..providers import AIProviderError
from ..config import settings
from .health import get_health_status


def create_app() -> Optional[Flask]:
    """
    Create and configure Flask application

    Returns:
        Configured Flask app or None if Flask not available
    """
    if not FLASK_AVAILABLE:
        print("ERROR: Flask not available. Install with: pip install Flask Flask-CORS")
        return None

    app = Flask(__name__)
    CORS(app)

    # =============================================================================
    # RESUME OPTIMIZATION ENDPOINTS
    # =============================================================================

    @app.route("/api/optimize", methods=["POST"])
    def optimize_resume():
        """Optimize resume based on job description"""
        try:
            data = request.get_json()

            if not data or "resumeData" not in data or "jobDescription" not in data:
                return jsonify({"error": "Missing resumeData or jobDescription"}), 400

            resume_data = data["resumeData"]
            job_description = data["jobDescription"]

            # Validate inputs
            resume_validation = ValidationService.validate_resume(resume_data)
            if not resume_validation.is_valid:
                return (
                    jsonify(
                        {
                            "error": "Invalid resume format",
                            "validation_errors": resume_validation.to_dict(),
                        }
                    ),
                    400,
                )

            job_validation = ValidationService.validate_job_description(job_description)
            if not job_validation["valid"]:
                return (
                    jsonify(
                        {
                            "error": "Invalid job description",
                            "validation_errors": job_validation,
                        }
                    ),
                    400,
                )

            # Optimize resume using service layer
            (
                default_html,
                optimized_html,
                customized_data,
                role_keywords,
            ) = ResumeService.optimize_resume(resume_data, job_description)

            # Calculate ATS scores
            default_score = ScoringService.calculate_ats_score(
                resume_data, role_keywords
            )
            optimized_score = ScoringService.calculate_ats_score(
                customized_data, role_keywords
            )

            # Generate optimization summary
            optimizations = ScoringService.generate_optimization_summary(
                resume_data, customized_data, role_keywords
            )

            return jsonify(
                {
                    "success": True,
                    "defaultHtml": default_html,
                    "optimizedHtml": optimized_html,
                    "defaultScore": default_score,
                    "optimizedScore": optimized_score,
                    "improvement": optimized_score - default_score,
                    "optimizations": optimizations,
                    "keywords": role_keywords[:20],  # Top 20 keywords
                }
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # =============================================================================
    # RESUME PARSING ENDPOINTS
    # =============================================================================

    @app.route("/api/parse-resume", methods=["POST"])
    def parse_text_resume():
        """Convert text resume to structured JSON using configurable AI provider"""
        try:
            data = request.get_json()
            if not data or "textResume" not in data:
                return jsonify({"error": "Missing textResume field"}), 400

            text_resume = data["textResume"].strip()

            # Use parsing service
            parsed_resume = ParsingService.parse_text_resume(text_resume)

            # Validate the parsed resume structure
            validation_result = ValidationService.validate_resume(parsed_resume)

            return jsonify(
                {
                    "success": True,
                    "resumeData": parsed_resume,
                    "validation": validation_result.to_dict(),
                    "message": "Resume successfully converted to structured JSON format",
                }
            )

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except AIProviderError as e:
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            return jsonify({"error": f"Resume parsing failed: {str(e)}"}), 500

    # =============================================================================
    # VALIDATION ENDPOINTS
    # =============================================================================

    @app.route("/api/validate-resume", methods=["POST"])
    def validate_resume():
        """Validate resume JSON structure"""
        try:
            data = request.get_json()
            if not data or "resumeData" not in data:
                return jsonify({"error": "Missing resumeData"}), 400

            resume_data = data["resumeData"]
            validation_result = ValidationService.validate_resume(resume_data)

            return jsonify(validation_result.to_dict())

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # =============================================================================
    # SAMPLE DATA ENDPOINTS
    # =============================================================================

    @app.route("/api/sample-resume", methods=["GET"])
    def get_sample_resume():
        """Get sample resume template"""
        try:
            # Load the existing resume as a template
            sample_path = settings.sample_resume_path
            if not sample_path.exists():
                return jsonify({"error": "Sample resume not found"}), 404

            with open(sample_path, "r") as f:
                sample_data = json.load(f)

            # Anonymize the sample data
            sample_data["personal"] = {
                "name": "Your Full Name",
                "email": "your.email@example.com",
                "phone": "+1 (555) 123-4567",
                "location": "Your City, State",
                "linkedin": "linkedin.com/in/yourprofile",
            }

            return jsonify(
                {
                    "success": True,
                    "sampleData": sample_data,
                    "instructions": {
                        "personal": "Required: Your contact information",
                        "summary": "Professional summary with headline and bullet points",
                        "experience": "Work history with achievements containing keywords and metrics",
                        "skills": "Technical skills organized by category and proficiency level",
                        "education": "Educational background",
                        "projects": "Key projects with descriptions and keywords",
                    },
                }
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # =============================================================================
    # PDF EXPORT ENDPOINTS
    # =============================================================================

    @app.route("/api/export-pdf", methods=["POST"])
    def export_pdf():
        """Export resume as PDF"""
        if not PDFKIT_AVAILABLE or not settings.pdf_export_enabled:
            return (
                jsonify(
                    {
                        "error": "PDF export not available. Install wkhtmltopdf and pdfkit."
                    }
                ),
                500,
            )

        try:
            data = request.get_json()
            if not data or "html" not in data:
                return jsonify({"error": "Missing HTML content"}), 400

            html_content = data["html"]
            filename = data.get("filename", "resume.pdf")

            # Configure PDF options
            options = {
                "page-size": "Letter",
                "margin-top": "0.5in",
                "margin-right": "0.5in",
                "margin-bottom": "0.5in",
                "margin-left": "0.5in",
                "encoding": "UTF-8",
                "no-outline": None,
                "enable-local-file-access": None,
            }

            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                pdf_path = tmp_file.name

            # Generate PDF
            pdfkit.from_string(html_content, pdf_path, options=options)

            # Clean up temp file after response is sent
            @after_this_request
            def cleanup(response):
                try:
                    os.unlink(pdf_path)
                except Exception as e:
                    # Log error but don't fail the response
                    print(f"Warning: Failed to delete temp file {pdf_path}: {e}")
                return response

            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=filename,
                mimetype="application/pdf",
            )

        except Exception as e:
            return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

    # =============================================================================
    # HEALTH CHECK ENDPOINTS
    # =============================================================================

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Enhanced health check endpoint with detailed system information"""
        return jsonify(get_health_status())

    @app.route("/", methods=["GET"])
    def root():
        """Root endpoint"""
        return jsonify(
            {
                "name": "ResumeForge API",
                "version": __version__,
                "status": "running",
                "endpoints": {
                    "health": "/api/health",
                    "optimize": "/api/optimize",
                    "parse": "/api/parse-resume",
                    "validate": "/api/validate-resume",
                    "sample": "/api/sample-resume",
                    "export": "/api/export-pdf",
                },
            }
        )

    return app
