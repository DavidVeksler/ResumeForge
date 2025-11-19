"""
Resume Generator - Main orchestrator for resume generation
"""

from typing import Dict, Any
from .template_renderer import TemplateRenderer
from .keyword_extractor import KeywordExtractor
from .relevance_scorer import RelevanceScorer


class ResumeGenerator:
    """
    Main class for resume generation

    This class orchestrates the various components to generate
    ATS-optimized HTML resumes from structured JSON data.
    """

    def __init__(self, resume_data: Dict[str, Any]):
        """
        Initialize resume generator

        Args:
            resume_data: Structured resume data dictionary
        """
        self.data = resume_data
        self.renderer = TemplateRenderer(resume_data)

    def generate_ats_template(self) -> str:
        """
        Generate modern, professional ATS-optimized HTML resume

        Returns:
            Complete HTML document as string
        """
        return self.renderer.render()

    def customize_for_role(
        self,
        job_description: str,
        role_keywords: list = None
    ) -> Dict[str, Any]:
        """
        Customize resume data for specific role

        Args:
            job_description: Job description text
            role_keywords: Pre-extracted keywords (optional)

        Returns:
            Customized resume data dictionary
        """
        # Extract keywords if not provided
        if role_keywords is None:
            extractor = KeywordExtractor(job_description)
            role_keywords = extractor.extract()

        # Score and customize resume
        scorer = RelevanceScorer(role_keywords, job_description)
        return scorer.customize_resume_data(self.data)


# Backward compatibility: expose extract_keywords_from_job_description at module level
def extract_keywords_from_job_description(job_description: str) -> list:
    """
    Extract relevant keywords from job description for resume customization

    Args:
        job_description: Job description text

    Returns:
        List of extracted keywords sorted by relevance
    """
    from .keyword_extractor import extract_keywords_from_job_description as extract
    return extract(job_description)
