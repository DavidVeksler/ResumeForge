"""
API request models
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class OptimizeRequest:
    """Request for resume optimization"""
    resumeData: Dict[str, Any]
    jobDescription: str


@dataclass
class ParseResumeRequest:
    """Request for text resume parsing"""
    textResume: str


@dataclass
class ValidateResumeRequest:
    """Request for resume validation"""
    resumeData: Dict[str, Any]


@dataclass
class ExportPDFRequest:
    """Request for PDF export"""
    html: str
    filename: str = "resume.pdf"
