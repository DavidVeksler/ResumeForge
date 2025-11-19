"""
Relevance Scorer - Score and rank achievements by job relevance
"""

from typing import Dict, List, Any


class RelevanceScorer:
    """Score and customize resume achievements for specific roles"""

    def __init__(self, role_keywords: List[str], job_description: str):
        """
        Initialize relevance scorer

        Args:
            role_keywords: Keywords extracted from job description
            job_description: Full job description text
        """
        self.role_keywords = role_keywords
        self.job_description = job_description.lower()
        self.keyword_weights = self._calculate_keyword_weights()

    def score_achievement(self, achievement: Dict[str, Any]) -> float:
        """
        Calculate relevance score for an achievement

        Args:
            achievement: Achievement dictionary with text and keywords

        Returns:
            Relevance score (higher is better)
        """
        score = 0.0

        achievement_keywords = achievement.get('keywords', [])
        achievement_text = achievement.get('text', '').lower()

        # Direct keyword matches with weights
        for kw in achievement_keywords:
            if kw.lower() in [rk.lower() for rk in self.role_keywords]:
                weight = self.keyword_weights.get(kw.lower(), 1.0)
                score += weight

        # Partial matches for compound keywords
        for role_kw in self.role_keywords:
            if role_kw.lower() in achievement_text:
                weight = self.keyword_weights.get(role_kw.lower(), 0.5)
                score += weight * 0.7  # Partial match weight

        # Boost score for quantified achievements
        if achievement.get('metrics'):
            score += 1.0

        return score

    def customize_resume_data(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Customize resume data for specific role

        Args:
            resume_data: Original resume data

        Returns:
            Customized resume data with scored and sorted achievements
        """
        customized_data = resume_data.copy()

        # Score all achievements
        for job in customized_data.get('experience', []):
            for achievement in job.get('achievements', []):
                achievement['relevance_score'] = self.score_achievement(achievement)

        # Sort achievements by relevance
        for job in customized_data.get('experience', []):
            achievements = job.get('achievements', [])
            achievements.sort(
                key=lambda x: x.get('relevance_score', 0),
                reverse=True
            )

            # Ensure at least one achievement has some relevance
            if achievements and achievements[0].get('relevance_score', 0) < 1:
                achievements[0]['relevance_score'] = 1.0

        # Add role-specific keywords
        if 'keywords' not in customized_data:
            customized_data['keywords'] = {}

        customized_data['keywords']['role_specific'] = self.role_keywords[:20]

        return customized_data

    def _calculate_keyword_weights(self) -> Dict[str, float]:
        """Calculate importance weights for keywords based on frequency and context"""
        keyword_weights = {}

        for keyword in self.role_keywords:
            kw_lower = keyword.lower()
            weight = 1.0

            # Count occurrences in job description
            occurrences = self.job_description.count(kw_lower)
            if occurrences > 1:
                weight += min(occurrences * 0.2, 1.0)  # Max bonus of 1.0

            # Higher weight for keywords in requirements sections
            requirement_contexts = [
                'required', 'must have', 'essential', 'mandatory',
                'experience with', 'proficient in', 'expertise in'
            ]

            for context in requirement_contexts:
                if context in self.job_description:
                    context_start = self.job_description.find(context)
                    context_end = context_start + 200
                    if kw_lower in self.job_description[context_start:context_end]:
                        weight += 0.5
                        break

            # Higher weight for high-value terms
            from config.patterns import HIGH_PRIORITY_TERMS
            if kw_lower in HIGH_PRIORITY_TERMS:
                weight += 0.3

            keyword_weights[kw_lower] = weight

        return keyword_weights
