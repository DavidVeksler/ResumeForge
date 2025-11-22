"""
Scoring Service - ATS scoring and optimization metrics
Consolidates logic from services/scoring_service.py
"""

from typing import Dict, Any, List, Set
import re

from config.patterns import PRIORITY_PATTERNS


class ScoringService:
    """Service for ATS scoring and optimization analysis"""

    @staticmethod
    def calculate_ats_score(resume_data: Dict[str, Any], keywords: List[str]) -> float:
        """
        Calculate ATS compatibility score

        Args:
            resume_data: Resume data
            keywords: List of keywords from job description

        Returns:
            ATS score (0-100)
        """
        if not keywords:
            return 0.0

        keyword_set = set(k.lower() for k in keywords)
        resume_text = ScoringService._extract_resume_text(resume_data)
        resume_text_lower = resume_text.lower()

        # Count keyword matches
        matches = sum(1 for keyword in keyword_set if keyword in resume_text_lower)

        # Calculate score
        match_percentage = (matches / len(keyword_set)) * 100

        # Bonus for structured data
        structure_bonus = 0
        if resume_data.get("experience"):
            structure_bonus += 5
        if resume_data.get("skills"):
            structure_bonus += 5
        if resume_data.get("education"):
            structure_bonus += 5

        final_score = min(100.0, match_percentage + structure_bonus)
        return round(final_score, 2)

    @staticmethod
    def extract_keywords_from_job_description(job_description: str) -> List[str]:
        """
        Extract keywords from job description

        Args:
            job_description: Job description text

        Returns:
            List of extracted keywords
        """
        keywords = set()
        job_lower = job_description.lower()

        # Extract keywords using priority patterns
        for pattern in PRIORITY_PATTERNS:
            matches = re.findall(pattern, job_lower, re.IGNORECASE)
            keywords.update(match.lower() for match in matches)

        # Extract from requirement phrases
        requirement_patterns = [
            r'(?:required|must have|should have|needs?)\s*:?\s*([^.;\n]+)',
            r'(?:experience (?:with|in))\s*:?\s*([^.;\n]+)',
            r'(?:proficient (?:with|in))\s*:?\s*([^.;\n]+)',
        ]
        for pattern in requirement_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            for match in matches:
                # Extract words from the requirement text
                words = re.findall(r'\b[a-zA-Z][\w+#.-]*\b', match)
                keywords.update(word.lower() for word in words if len(word) > 2)

        # Common tech skills (basic extraction)
        tech_terms = [
            'python', 'javascript', 'react', 'node', 'sql', 'aws', 'docker',
            'kubernetes', 'api', 'rest', 'agile', 'scrum', 'git', 'ci/cd',
            'typescript', 'mongodb', 'postgres', 'redis', 'graphql', 'flask',
            'django', 'fastapi', 'blockchain', 'ethereum', 'defi', 'smart contracts',
            'web3', 'solidity', 'nft', 'cryptocurrency', 'fintech', 'payment',
            'trading', 'financial', 'banking'
        ]

        for term in tech_terms:
            if term in job_lower:
                keywords.add(term)

        return sorted(list(keywords))

    @staticmethod
    def generate_optimization_summary(
        original_data: Dict[str, Any],
        optimized_data: Dict[str, Any],
        keywords: List[str],
    ) -> Dict[str, Any]:
        """
        Generate summary of optimizations made

        Args:
            original_data: Original resume data
            optimized_data: Optimized resume data
            keywords: Keywords from job description

        Returns:
            Dictionary with optimization details
        """
        return {
            "keywords_added": len(keywords),
            "achievements_reordered": ScoringService._count_reordered_achievements(
                original_data, optimized_data
            ),
            "relevance_scoring_applied": True,
            "ats_keywords_injected": True,
        }

    @staticmethod
    def _extract_resume_text(resume_data: Dict[str, Any]) -> str:
        """Extract all text from resume for keyword matching"""
        text_parts = []

        # Personal section
        if "personal" in resume_data:
            personal = resume_data["personal"]
            text_parts.extend([
                personal.get("name", ""),
                personal.get("location", ""),
            ])

        # Summary
        if "summary" in resume_data:
            summary = resume_data["summary"]
            text_parts.append(summary.get("headline", ""))
            text_parts.extend(summary.get("bullets", []))

        # Experience
        if "experience" in resume_data:
            for job in resume_data["experience"]:
                text_parts.extend([
                    job.get("title", ""),
                    job.get("company", ""),
                    job.get("description", ""),
                ])
                for achievement in job.get("achievements", []):
                    text_parts.append(achievement.get("text", ""))
                    text_parts.extend(achievement.get("keywords", []))

        # Skills
        if "skills" in resume_data:
            skills = resume_data["skills"]
            for category, skill_data in skills.items():
                if isinstance(skill_data, dict):
                    for level, items in skill_data.items():
                        if isinstance(items, list):
                            text_parts.extend(items)
                elif isinstance(skill_data, list):
                    text_parts.extend(skill_data)

        # Projects
        if "projects" in resume_data:
            for project in resume_data["projects"]:
                text_parts.append(project.get("name", ""))
                text_parts.append(project.get("description", ""))
                text_parts.extend(project.get("keywords", []))
                text_parts.extend(project.get("technologies", []))

        return " ".join(str(part) for part in text_parts if part)

    @staticmethod
    def _count_reordered_achievements(
        original: Dict[str, Any], optimized: Dict[str, Any]
    ) -> int:
        """Count number of achievements that were reordered"""
        count = 0

        original_exp = original.get("experience", [])
        optimized_exp = optimized.get("experience", [])

        for orig_job, opt_job in zip(original_exp, optimized_exp):
            orig_achievements = orig_job.get("achievements", [])
            opt_achievements = opt_job.get("achievements", [])

            # Check if order changed
            if len(orig_achievements) == len(opt_achievements):
                for i, (orig, opt) in enumerate(zip(orig_achievements, opt_achievements)):
                    if orig.get("text") != opt.get("text"):
                        count += 1

        return count
