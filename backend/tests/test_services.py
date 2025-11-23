"""
Service layer tests
"""

import pytest
import json

from backend.services import (
    ResumeService,
    ScoringService,
    ValidationService,
)
from backend.config import settings


@pytest.fixture
def sample_resume():
    """Load sample resume data"""
    sample_path = settings.sample_resume_path
    if not sample_path.exists():
        pytest.skip("Sample resume not found")

    with open(sample_path, "r") as f:
        return json.load(f)


class TestValidationService:
    """Test validation service"""

    def test_validate_valid_resume(self, sample_resume):
        """Test validation with valid resume"""
        result = ValidationService.validate_resume(sample_resume)
        assert result.is_valid

    def test_validate_empty_resume(self):
        """Test validation with empty resume"""
        result = ValidationService.validate_resume({})
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_validate_missing_personal(self):
        """Test validation with missing personal section"""
        resume = {"experience": [], "skills": {}}
        result = ValidationService.validate_resume(resume)
        assert not result.is_valid
        assert any("personal" in error.lower() for error in result.errors)

    def test_validate_job_description(self):
        """Test job description validation"""
        valid_job = "We are seeking a Python developer with 5+ years of experience."
        result = ValidationService.validate_job_description(valid_job)
        assert result["valid"]

    def test_validate_empty_job_description(self):
        """Test empty job description"""
        result = ValidationService.validate_job_description("")
        assert not result["valid"]


class TestScoringService:
    """Test scoring service"""

    def test_calculate_ats_score(self, sample_resume):
        """Test ATS score calculation"""
        keywords = ["python", "javascript", "react", "aws"]
        score = ScoringService.calculate_ats_score(sample_resume, keywords)
        assert 0 <= score <= 100

    def test_calculate_ats_score_no_keywords(self, sample_resume):
        """Test ATS score with no keywords"""
        score = ScoringService.calculate_ats_score(sample_resume, [])
        assert score == 0.0

    def test_extract_keywords(self):
        """Test keyword extraction"""
        job_desc = """
        Required skills: Python, JavaScript, React, Docker, Kubernetes
        Experience with AWS, CI/CD, and Agile methodologies
        """
        keywords = ScoringService.extract_keywords_from_job_description(job_desc)
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert "python" in [k.lower() for k in keywords]


class TestResumeService:
    """Test resume service"""

    def test_generate_resume(self, sample_resume):
        """Test resume HTML generation"""
        html = ResumeService.generate_resume(sample_resume)
        assert isinstance(html, str)
        assert len(html) > 0
        assert "<!DOCTYPE html>" in html or "<html" in html

    def test_optimize_resume(self, sample_resume):
        """Test resume optimization"""
        job_description = """
        We need a Python developer with experience in:
        - Web development with Flask/Django
        - REST API design
        - Cloud deployment (AWS)
        """

        result = ResumeService.optimize_resume(sample_resume, job_description)
        assert len(result) == 4

        default_html, optimized_html, customized_data, keywords = result
        assert isinstance(default_html, str)
        assert isinstance(optimized_html, str)
        assert isinstance(customized_data, dict)
        assert isinstance(keywords, list)
