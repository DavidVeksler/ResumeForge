"""
Resume Service - Handles resume generation and optimization
Consolidates logic from services/resume_service.py and resume/generator.py
"""

from typing import Dict, Any, Tuple, List
from resume.generator import ResumeGenerator, extract_keywords_from_job_description


class ResumeService:
    """Service for resume generation and optimization"""

    @staticmethod
    def optimize_resume(
        resume_data: Dict[str, Any], job_description: str
    ) -> Tuple[str, str, Dict[str, Any], List[str]]:
        """
        Optimize resume for a specific job description

        Args:
            resume_data: Structured resume data
            job_description: Job description text

        Returns:
            Tuple of (default_html, optimized_html, customized_data, role_keywords)
        """
        # Create resume generator
        generator = ResumeGenerator(resume_data)

        # Extract keywords from job description
        role_keywords = extract_keywords_from_job_description(job_description)

        # Generate default resume
        default_html = generator.generate_ats_template()

        # Customize for role and generate optimized resume
        customized_data = generator.customize_for_role(job_description, role_keywords)
        optimized_generator = ResumeGenerator(customized_data)
        optimized_html = optimized_generator.generate_ats_template()

        return default_html, optimized_html, customized_data, role_keywords

    @staticmethod
    def generate_resume(resume_data: Dict[str, Any], template: str = "ats") -> str:
        """
        Generate HTML resume from structured data

        Args:
            resume_data: Structured resume data
            template: Template type (default: 'ats')

        Returns:
            Generated HTML content
        """
        generator = ResumeGenerator(resume_data)

        if template == "ats":
            return generator.generate_ats_template()
        else:
            raise ValueError(f"Unknown template type: {template}")

    @staticmethod
    def customize_for_job(
        resume_data: Dict[str, Any],
        job_description: str,
        role_keywords: List[str],
    ) -> Dict[str, Any]:
        """
        Customize resume data for a specific job

        Args:
            resume_data: Original resume data
            job_description: Job description text
            role_keywords: Extracted keywords from job

        Returns:
            Customized resume data
        """
        generator = ResumeGenerator(resume_data)
        return generator.customize_for_role(job_description, role_keywords)
