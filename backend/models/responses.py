"""
API response models
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class OptimizeResponse:
    """Response from resume optimization"""
    success: bool
    defaultHtml: str
    optimizedHtml: str
    defaultScore: float
    optimizedScore: float
    improvement: float
    optimizations: Dict[str, Any]
    keywords: List[str]
    error: Optional[str] = None


@dataclass
class ParseResumeResponse:
    """Response from text resume parsing"""
    success: bool
    resumeData: Optional[Dict[str, Any]] = None
    validation: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ValidationResponse:
    """Response from validation"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class HealthResponse:
    """Health check response"""
    status: str
    version: str
    python_version: str
    flask_version: Optional[str] = None
    ai_provider: Optional[str] = None
    pdf_export_available: bool = False
    timestamp: Optional[str] = None
