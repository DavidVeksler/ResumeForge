"""
Skills Processor - Handle skill variations and keyword generation
"""

from typing import List
from config.patterns import TECH_VARIATIONS, HIGH_PRIORITY_TERMS


class SkillsProcessor:
    """Process skills for resume generation and ATS optimization"""

    @staticmethod
    def get_skill_variations(skill: str) -> List[str]:
        """
        Get common variations and synonyms for skills

        Args:
            skill: Skill name

        Returns:
            List of skill variations
        """
        skill_lower = skill.lower()

        if skill_lower in TECH_VARIATIONS:
            return TECH_VARIATIONS[skill_lower]

        return []

    @staticmethod
    def is_high_priority(keyword: str) -> bool:
        """
        Determine if a keyword should be repeated for better ATS recognition

        Args:
            keyword: Keyword to check

        Returns:
            True if keyword is high priority
        """
        return keyword.lower() in HIGH_PRIORITY_TERMS

    @staticmethod
    def extract_skill_keywords(skills: dict) -> List[str]:
        """
        Extract all skills from skills dictionary

        Args:
            skills: Skills dictionary from resume data

        Returns:
            List of all skills
        """
        keywords = []

        for skill_category in skills.values():
            if isinstance(skill_category, dict):
                for skill_list in skill_category.values():
                    if isinstance(skill_list, list):
                        keywords.extend(skill_list)
                        # Add variations
                        for skill in skill_list:
                            keywords.extend(
                                SkillsProcessor.get_skill_variations(skill)
                            )
            elif isinstance(skill_category, list):
                keywords.extend(skill_category)
                for skill in skill_category:
                    keywords.extend(
                        SkillsProcessor.get_skill_variations(skill)
                    )

        return keywords
