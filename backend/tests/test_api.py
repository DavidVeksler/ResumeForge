"""
API endpoint tests
Consolidated from integration_test.py and test_mock_api.py
"""

import json
import pytest
from pathlib import Path

from backend.api import create_app
from backend.config import settings


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    if app is None:
        pytest.skip("Flask not available")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_resume():
    """Load sample resume data"""
    sample_path = settings.sample_resume_path
    if not sample_path.exists():
        pytest.skip("Sample resume not found")

    with open(sample_path, "r") as f:
        return json.load(f)


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test /api/health endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = response.get_json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "python_version" in data


class TestValidationEndpoint:
    """Test validation endpoint"""

    def test_validate_resume_valid(self, client, sample_resume):
        """Test validation with valid resume"""
        response = client.post(
            "/api/validate-resume",
            json={"resumeData": sample_resume},
            content_type="application/json",
        )
        assert response.status_code == 200

        data = response.get_json()
        assert "valid" in data

    def test_validate_resume_missing_data(self, client):
        """Test validation with missing data"""
        response = client.post(
            "/api/validate-resume",
            json={},
            content_type="application/json",
        )
        assert response.status_code == 400


class TestSampleResumeEndpoint:
    """Test sample resume endpoint"""

    def test_get_sample_resume(self, client):
        """Test /api/sample-resume endpoint"""
        response = client.get("/api/sample-resume")

        if response.status_code == 404:
            pytest.skip("Sample resume not found")

        assert response.status_code == 200
        data = response.get_json()
        assert "sampleData" in data
        assert "instructions" in data


class TestOptimizationEndpoint:
    """Test optimization endpoint"""

    def test_optimize_resume_missing_data(self, client):
        """Test optimization with missing data"""
        response = client.post(
            "/api/optimize",
            json={},
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_optimize_resume_valid(self, client, sample_resume):
        """Test optimization with valid data"""
        job_description = """
        We are seeking a Senior Full Stack Developer with experience in:
        - Python, JavaScript, React, Node.js
        - REST APIs and microservices
        - Cloud platforms (AWS, Azure)
        - Agile development methodologies

        Requirements:
        - 5+ years of software development experience
        - Strong knowledge of web technologies
        - Experience with CI/CD pipelines
        """

        response = client.post(
            "/api/optimize",
            json={
                "resumeData": sample_resume,
                "jobDescription": job_description,
            },
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "defaultHtml" in data
        assert "optimizedHtml" in data
        assert "defaultScore" in data
        assert "optimizedScore" in data


class TestRootEndpoint:
    """Test root endpoint"""

    def test_root_endpoint(self, client):
        """Test / endpoint"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.get_json()
        assert data["name"] == "ResumeForge API"
        assert "endpoints" in data
