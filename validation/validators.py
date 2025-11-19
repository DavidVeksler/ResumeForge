"""
Validators - Input validation for resumes and job descriptions
"""

import re
from typing import Dict, List, Any


class ValidationResult:
    """Container for validation results"""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.recommendations: List[str] = []

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)"""
        return len(self.errors) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'valid': self.is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'recommendations': self.recommendations if self.is_valid else []
        }


class ResumeValidator:
    """Validator for resume JSON structure"""

    @staticmethod
    def validate(resume_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate resume JSON structure

        Args:
            resume_data: Resume data to validate

        Returns:
            ValidationResult with errors, warnings, and recommendations
        """
        result = ValidationResult()

        if not isinstance(resume_data, dict):
            result.errors.append('Resume data must be a JSON object')
            return result

        ResumeValidator._validate_personal_section(resume_data, result)
        ResumeValidator._validate_experience_section(resume_data, result)
        ResumeValidator._validate_skills_section(resume_data, result)
        ResumeValidator._validate_summary_section(resume_data, result)

        if result.is_valid:
            result.recommendations = [
                'Include quantifiable achievements with metrics (e.g., "$100M TVL", "20+ engineers")',
                'Add relevant keywords to each achievement for better ATS matching',
                'Organize skills by proficiency level (expert, proficient, familiar)',
                'Include education section for complete professional profile'
            ]

        return result

    @staticmethod
    def _validate_personal_section(
        resume_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate personal information section"""
        if 'personal' not in resume_data:
            result.errors.append('Missing required "personal" section')
            return

        personal = resume_data['personal']
        required_fields = ['name', 'email']

        for field in required_fields:
            if field not in personal or not personal[field]:
                result.errors.append(f'Missing required personal.{field}')

        # Email validation
        if 'email' in personal and personal['email']:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, personal['email']):
                result.errors.append('Invalid email format in personal.email')

    @staticmethod
    def _validate_experience_section(
        resume_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate experience section"""
        if 'experience' not in resume_data:
            result.warnings.append(
                'Missing "experience" section - recommended for ATS optimization'
            )
            return

        experience = resume_data['experience']

        if not isinstance(experience, list):
            result.errors.append('"experience" must be an array of job objects')
            return

        for i, job in enumerate(experience):
            if not isinstance(job, dict):
                result.errors.append(f'Experience item {i+1} must be an object')
                continue

            required_job_fields = ['title', 'company', 'duration']
            for field in required_job_fields:
                if field not in job or not job[field]:
                    result.warnings.append(
                        f'Experience item {i+1} missing recommended field: {field}'
                    )

            if 'achievements' in job:
                ResumeValidator._validate_achievements(
                    job['achievements'],
                    i,
                    result
                )

    @staticmethod
    def _validate_achievements(
        achievements: Any,
        job_index: int,
        result: ValidationResult
    ) -> None:
        """Validate achievements array"""
        if not isinstance(achievements, list):
            result.errors.append(
                f'Experience item {job_index+1} achievements must be an array'
            )
            return

        for j, achievement in enumerate(achievements):
            if not isinstance(achievement, dict) or 'text' not in achievement:
                result.errors.append(
                    f'Achievement {j+1} in job {job_index+1} must have "text" field'
                )

    @staticmethod
    def _validate_skills_section(
        resume_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate skills section"""
        if 'skills' not in resume_data:
            result.warnings.append(
                'Missing "skills" section - important for ATS scoring'
            )

    @staticmethod
    def _validate_summary_section(
        resume_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate summary section"""
        if 'summary' not in resume_data:
            result.warnings.append(
                'Missing "summary" section - helps with ATS optimization'
            )
            return

        summary = resume_data['summary']
        if 'headline' not in summary or not summary['headline']:
            result.warnings.append(
                'Missing summary headline - recommended for professional impact'
            )


class JobDescriptionValidator:
    """Validator for job description text"""

    MIN_WORD_COUNT = 50
    MAX_WORD_COUNT = 2000

    @staticmethod
    def validate(job_description: str) -> Dict[str, Any]:
        """
        Validate job description input

        Args:
            job_description: Job description text

        Returns:
            Dictionary with validation results
        """
        result = ValidationResult()

        if not job_description or not job_description.strip():
            result.errors.append('Job description cannot be empty')
            return result.to_dict()

        word_count = len(job_description.split())

        # Length validation
        if word_count < JobDescriptionValidator.MIN_WORD_COUNT:
            result.warnings.append(
                f'Job description is quite short ({word_count} words). '
                'Longer descriptions provide better optimization.'
            )
        elif word_count > JobDescriptionValidator.MAX_WORD_COUNT:
            result.warnings.append(
                f'Job description is very long ({word_count} words). '
                'Consider focusing on key requirements.'
            )

        # Content validation
        common_sections = [
            'requirements', 'responsibilities', 'qualifications',
            'skills', 'experience'
        ]
        found_sections = sum(
            1 for section in common_sections
            if section.lower() in job_description.lower()
        )

        if found_sections < 2:
            result.warnings.append(
                'Job description may be missing key sections '
                '(requirements, responsibilities, qualifications)'
            )

        # Technical terms check
        technical_indicators = [
            'years', 'experience', 'required', 'preferred',
            'must have', 'should have'
        ]
        found_indicators = sum(
            1 for indicator in technical_indicators
            if indicator.lower() in job_description.lower()
        )

        if found_indicators < 2:
            result.warnings.append(
                'Job description may lack specific requirements '
                'for better keyword extraction'
            )

        response = result.to_dict()
        response['word_count'] = word_count
        response['estimated_keywords'] = min(60, word_count // 10)

        return response
