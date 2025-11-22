"""
Health check utilities
Consolidated from routes/health_routes.py
"""

import sys
from datetime import datetime
from typing import Dict, Any

from ..config import settings


def get_health_status() -> Dict[str, Any]:
    """
    Get comprehensive health status

    Returns:
        Dictionary with system health information
    """
    # Get Flask version if available
    flask_version = None
    try:
        import flask
        flask_version = flask.__version__
    except ImportError:
        pass

    # Get OpenAI package availability
    openai_available = False
    try:
        import openai
        openai_available = True
    except ImportError:
        pass

    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "flask_version": flask_version,
        "ai_provider": {
            "configured": settings.ai.provider,
            "model": (
                settings.ai.openai_model
                if settings.ai.provider == "openai"
                else settings.ai.local_model_name
            ),
            "openai_available": openai_available,
        },
        "features": {
            "pdf_export": settings.pdf_export_enabled,
            "ai_parsing": openai_available,
        },
        "environment": settings.flask.env,
    }
