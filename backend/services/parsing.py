"""
Parsing Service - Text-to-JSON conversion using AI providers
Consolidates AI parsing logic
"""

from typing import Dict, Any, Optional

from ..providers import create_ai_provider, AIProviderError


class ParsingService:
    """Service for text resume parsing"""

    @staticmethod
    def parse_text_resume(text_resume: str, provider_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert text resume to structured JSON using AI

        Args:
            text_resume: Raw text resume content
            provider_type: Optional provider override ('openai' or 'local')

        Returns:
            Parsed resume data as dictionary

        Raises:
            AIProviderError: If parsing fails
            ValueError: If input is invalid
        """
        if not text_resume or not text_resume.strip():
            raise ValueError("Text resume cannot be empty")

        # Create AI provider
        provider = create_ai_provider(provider_type)

        # Parse resume
        parsed_data = provider.parse_resume_text(text_resume)

        return parsed_data

    @staticmethod
    def test_ai_provider(provider_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Test AI provider connectivity

        Args:
            provider_type: Optional provider type ('openai' or 'local')

        Returns:
            Test results dictionary
        """
        try:
            provider = create_ai_provider(provider_type)
            return provider.test_connectivity()
        except AIProviderError as e:
            return {
                "success": False,
                "error": str(e),
            }
