"""
AI Provider tests
Consolidated from test_ai_providers.py
"""

import pytest

from backend.providers import create_ai_provider, AIProviderError
from backend.config import settings


class TestAIProviderFactory:
    """Test AI provider factory"""

    def test_create_openai_provider(self):
        """Test creating OpenAI provider"""
        if not settings.ai.openai_api_key:
            pytest.skip("OpenAI API key not configured")

        try:
            provider = create_ai_provider("openai")
            assert provider.provider_name == "openai"
            assert provider.model_name == settings.ai.openai_model
        except AIProviderError as e:
            pytest.skip(f"OpenAI provider not available: {e}")

    def test_create_local_provider(self):
        """Test creating local provider"""
        try:
            provider = create_ai_provider("local")
            assert provider.provider_name == "local"
            assert provider.model_name == settings.ai.local_model_name
        except AIProviderError as e:
            pytest.skip(f"Local provider not available: {e}")

    def test_create_invalid_provider(self):
        """Test creating invalid provider"""
        with pytest.raises(AIProviderError):
            create_ai_provider("invalid")


class TestProviderConnectivity:
    """Test provider connectivity"""

    def test_openai_connectivity(self):
        """Test OpenAI provider connectivity"""
        if not settings.ai.openai_api_key:
            pytest.skip("OpenAI API key not configured")

        try:
            provider = create_ai_provider("openai")
            result = provider.test_connectivity()
            # Don't assert success - just check structure
            assert "success" in result
            assert "provider" in result
        except AIProviderError as e:
            pytest.skip(f"OpenAI provider not available: {e}")

    def test_local_connectivity(self):
        """Test local provider connectivity"""
        try:
            provider = create_ai_provider("local")
            result = provider.test_connectivity()
            # Don't assert success - just check structure
            assert "success" in result
            assert "provider" in result
        except AIProviderError as e:
            pytest.skip(f"Local provider not available: {e}")


class TestResumeParsingMock:
    """Test resume parsing with mock data"""

    def test_parse_empty_resume(self):
        """Test parsing empty resume"""
        if not settings.ai.openai_api_key:
            pytest.skip("OpenAI API key not configured")

        try:
            provider = create_ai_provider()
            with pytest.raises((ValueError, AIProviderError)):
                provider.parse_resume_text("")
        except AIProviderError as e:
            pytest.skip(f"Provider not available: {e}")

    def test_parse_simple_resume(self):
        """Test parsing simple resume text"""
        if not settings.ai.openai_api_key:
            pytest.skip("OpenAI API key not configured")

        simple_resume = """
        John Doe
        john@example.com

        Software Developer with 5 years of experience in Python and JavaScript.

        Experience:
        - Senior Developer at Tech Corp (2020-2023)
        - Junior Developer at StartupCo (2018-2020)

        Skills: Python, JavaScript, React, AWS

        Education:
        BS Computer Science, University of Tech, 2018
        """

        try:
            provider = create_ai_provider()
            result = provider.parse_resume_text(simple_resume)
            assert isinstance(result, dict)
            # Basic structure check
            assert "personal" in result or "experience" in result
        except AIProviderError as e:
            pytest.skip(f"AI parsing not available: {e}")
