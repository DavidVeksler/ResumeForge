"""
AI Provider Factory
Creates appropriate AI provider based on configuration
"""

from typing import Optional

from .base import AIProvider, AIProviderError
from .openai_provider import OpenAIProvider
from .local_provider import LocalLLMProvider
from ..config import settings


def create_ai_provider(provider_type: Optional[str] = None) -> AIProvider:
    """
    Create an AI provider instance based on configuration

    Args:
        provider_type: Override provider type ('openai' or 'local')
                      If None, uses settings.ai.provider

    Returns:
        AIProvider instance

    Raises:
        AIProviderError: If provider configuration is invalid
    """
    provider = provider_type or settings.ai.provider

    if provider == "openai":
        if not settings.ai.openai_api_key:
            raise AIProviderError(
                "OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
            )
        return OpenAIProvider(
            api_key=settings.ai.openai_api_key,
            model=settings.ai.openai_model,
        )

    elif provider == "local":
        return LocalLLMProvider(
            base_url=settings.ai.local_base_url,
            model=settings.ai.local_model_name,
        )

    else:
        raise AIProviderError(
            f"Unknown AI provider: {provider}. Must be 'openai' or 'local'."
        )
