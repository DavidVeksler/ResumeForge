"""
Base AI Provider Interface
Defines the contract for all AI provider implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class AIProviderError(Exception):
    """Raised when AI provider encounters an error"""
    pass


class AIProvider(ABC):
    """Abstract base class for AI providers"""

    @abstractmethod
    def parse_resume_text(self, text_resume: str) -> Dict[str, Any]:
        """
        Convert text resume to structured JSON format

        Args:
            text_resume: Raw text resume content

        Returns:
            Parsed resume data as dictionary

        Raises:
            AIProviderError: If parsing fails
            ValueError: If input is invalid
        """
        pass

    @abstractmethod
    def test_connectivity(self) -> Dict[str, Any]:
        """
        Test AI provider connectivity

        Returns:
            Dictionary with test results including success status
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the provider name"""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the model name"""
        pass
