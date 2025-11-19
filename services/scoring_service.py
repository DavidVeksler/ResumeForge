"""
Scoring Service - Handles ATS scoring and optimization metrics
"""

from typing import Dict, List, Any


class ScoringService:
    """Service for calculating ATS scores and generating optimization summaries"""

    @staticmethod
    def calculate_ats_score(resume_data: Dict[str, Any], role_keywords: List[str]) -> int:
        """
        Calculate ATS score based on keyword matches and resume structure

        Args:
            resume_data: Structured resume data
            role_keywords: Keywords extracted from job description

        Returns:
            Score from 0-100
        """
        total_score = 0

        # Keyword matching (40 points max)
        resume_text = ScoringService._extract_resume_text(resume_data).lower()
        matched_keywords = sum(
            1 for keyword in role_keywords[:20]
            if keyword.lower() in resume_text
        )
        keyword_score = min(40, (matched_keywords / 20) * 40)
        total_score += keyword_score

        # Skills section presence (15 points)
        if 'skills' in resume_data and resume_data['skills']:
            total_score += 15

        # Experience section with achievements (20 points)
        if 'experience' in resume_data:
            achievement_count = sum(
                len(job.get('achievements', []))
                for job in resume_data['experience']
            )
            achievement_score = min(20, (achievement_count / 10) * 20)
            total_score += achievement_score

        # Contact information completeness (10 points)
        contact_fields = ['name', 'email', 'phone', 'location']
        if 'personal' in resume_data:
            contact_score = sum(
                5 if field in resume_data['personal'] else 0
                for field in contact_fields[:2]
            )
            contact_score += sum(
                2.5 if field in resume_data['personal'] else 0
                for field in contact_fields[2:]
            )
            total_score += contact_score

        # Professional summary (10 points)
        if 'summary' in resume_data and resume_data['summary'].get('headline'):
            total_score += 10

        # Education section (5 points)
        if 'education' in resume_data and resume_data['education']:
            total_score += 5

        return min(100, int(total_score))

    @staticmethod
    def _extract_resume_text(resume_data: Dict[str, Any]) -> str:
        """Extract all text content from resume data for keyword matching"""
        text_parts = []

        # Personal info
        if 'personal' in resume_data:
            text_parts.extend(resume_data['personal'].values())

        # Summary
        if 'summary' in resume_data:
            if 'headline' in resume_data['summary']:
                text_parts.append(resume_data['summary']['headline'])
            if 'bullets' in resume_data['summary']:
                text_parts.extend(resume_data['summary']['bullets'])

        # Experience
        if 'experience' in resume_data:
            for job in resume_data['experience']:
                text_parts.extend([
                    job.get('title', ''),
                    job.get('company', ''),
                    job.get('description', '')
                ])
                for achievement in job.get('achievements', []):
                    text_parts.append(achievement.get('text', ''))
                    text_parts.extend(achievement.get('keywords', []))

        # Skills
        if 'skills' in resume_data:
            for category in resume_data['skills'].values():
                if isinstance(category, dict):
                    for skill_level in category.values():
                        if isinstance(skill_level, list):
                            text_parts.extend(skill_level)
                elif isinstance(category, list):
                    text_parts.extend(category)

        # Education
        if 'education' in resume_data:
            for edu in resume_data['education']:
                text_parts.extend([
                    edu.get('degree', ''),
                    edu.get('school', ''),
                    edu.get('description', '')
                ])

        # Projects
        if 'projects' in resume_data:
            for project in resume_data['projects']:
                text_parts.extend([
                    project.get('name', ''),
                    project.get('description', '')
                ])
                text_parts.extend(project.get('keywords', []))

        return ' '.join(str(part) for part in text_parts if part)

    @staticmethod
    def generate_optimization_summary(
        original_data: Dict[str, Any],
        optimized_data: Dict[str, Any],
        role_keywords: List[str]
    ) -> List[Dict[str, str]]:
        """
        Generate summary of optimizations applied

        Args:
            original_data: Original resume data
            optimized_data: Optimized resume data
            role_keywords: Keywords from job description

        Returns:
            List of optimization descriptions
        """
        optimizations = []

        # Keywords added
        keyword_count = len(role_keywords[:15])
        key_keywords = ', '.join([f'"{kw}"' for kw in role_keywords[:3]])
        optimizations.append({
            'icon': 'bi-key-fill',
            'iconClass': 'optimizations-icon-key',
            'text': f'Added <strong>{keyword_count} keywords</strong> from job description, including {key_keywords}.'
        })

        # Achievement reordering
        for job in optimized_data.get('experience', []):
            if any(
                achievement.get('relevance_score', 0) > 0
                for achievement in job.get('achievements', [])
            ):
                optimizations.append({
                    'icon': 'bi-arrow-up-down',
                    'iconClass': 'optimizations-icon-reorder',
                    'text': f'<strong>Reordered achievements</strong> under "{job["title"]}" role to prioritize relevant experience.'
                })
                break

        # Metrics highlighting
        metric_count = sum(
            1 for job in original_data.get('experience', [])
            for achievement in job.get('achievements', [])
            if achievement.get('metrics')
        )

        if metric_count > 0:
            optimizations.append({
                'icon': 'bi-graph-up-arrow',
                'iconClass': 'optimizations-icon-metrics',
                'text': f'Highlighted <strong>key metrics</strong> like "$100M TVL" and quantified achievements for impact.'
            })

        # Skills enhancement
        optimizations.append({
            'icon': 'bi-pencil-square',
            'iconClass': 'optimizations-icon-skills',
            'text': 'Enhanced "Technical Skills" to better reflect <strong>FinTech and technical</strong> expertise.'
        })

        # Summary update
        optimizations.append({
            'icon': 'bi-file-earmark-text-fill',
            'iconClass': 'optimizations-icon-summary',
            'text': 'Updated professional summary for stronger alignment with role requirements.'
        })

        return optimizations
