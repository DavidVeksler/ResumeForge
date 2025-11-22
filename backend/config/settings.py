"""
Centralized Configuration Management
Consolidates all environment variables and application settings
"""

import os
from typing import Literal, Optional
from pathlib import Path
from dataclasses import dataclass

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Continue with system environment variables


@dataclass
class AIProviderConfig:
    """AI Provider configuration"""
    provider: Literal["openai", "local"] = "openai"

    # OpenAI settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"

    # Local LLM settings
    local_base_url: str = "http://172.28.144.1:1234/v1"
    local_model_name: str = "local-model"

    @classmethod
    def from_env(cls) -> "AIProviderConfig":
        """Create configuration from environment variables"""
        return cls(
            provider=os.getenv("AI_PROVIDER", "openai").lower(),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            local_base_url=os.getenv("LOCAL_LLM_BASE_URL", "http://172.28.144.1:1234/v1"),
            local_model_name=os.getenv("LOCAL_MODEL_NAME", "local-model"),
        )


@dataclass
class FlaskConfig:
    """Flask application configuration"""
    host: str = "127.0.0.1"
    port: int = 5000
    debug: bool = True
    env: str = "development"

    @classmethod
    def from_env(cls) -> "FlaskConfig":
        """Create configuration from environment variables"""
        return cls(
            host=os.getenv("FLASK_HOST", "127.0.0.1"),
            port=int(os.getenv("FLASK_PORT", "5000")),
            debug=os.getenv("FLASK_DEBUG", "True").lower() == "true",
            env=os.getenv("FLASK_ENV", "development"),
        )


@dataclass
class AppSettings:
    """Application-wide settings"""

    # Base paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"

    # Configuration objects
    ai: AIProviderConfig = None
    flask: FlaskConfig = None

    # Feature flags
    pdf_export_enabled: bool = True

    def __post_init__(self):
        """Initialize nested configurations"""
        if self.ai is None:
            self.ai = AIProviderConfig.from_env()
        if self.flask is None:
            self.flask = FlaskConfig.from_env()

        # Check PDF export availability
        try:
            import pdfkit
            self.pdf_export_enabled = True
        except ImportError:
            self.pdf_export_enabled = False

    @property
    def sample_resume_path(self) -> Path:
        """Path to sample resume JSON"""
        return self.base_dir / "david_resume_json.json"


# Global settings instance
settings = AppSettings()
