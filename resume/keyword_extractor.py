"""
Keyword Extractor - Extract keywords from job descriptions and resumes
"""

import re
from typing import List
from config.patterns import PRIORITY_PATTERNS, STOP_WORDS


class KeywordExtractor:
    """Extract and score keywords from job descriptions"""

    MAX_KEYWORDS = 60

    def __init__(self, job_description: str):
        """
        Initialize keyword extractor

        Args:
            job_description: Job description text to extract keywords from
        """
        self.job_description = job_description
        self.text_lower = job_description.lower()
        self.keyword_scores = {}

    def extract(self) -> List[str]:
        """
        Extract keywords from job description

        Returns:
            List of keywords sorted by relevance
        """
        self._extract_priority_keywords()
        self._extract_technical_terms()
        self._extract_requirement_phrases()
        self._extract_tech_stack()

        # Filter and sort keywords
        filtered_keywords = self._filter_keywords()
        sorted_keywords = sorted(
            filtered_keywords,
            key=lambda x: self.keyword_scores[x],
            reverse=True
        )

        return sorted_keywords[:self.MAX_KEYWORDS]

    def _extract_priority_keywords(self) -> None:
        """Extract keywords using priority patterns"""
        for i, pattern in enumerate(PRIORITY_PATTERNS):
            matches = re.findall(pattern, self.text_lower, re.IGNORECASE)
            for match in matches:
                if match not in self.keyword_scores:
                    self.keyword_scores[match] = 0
                # Higher score for patterns that appear earlier (more important)
                self.keyword_scores[match] += (len(PRIORITY_PATTERNS) - i)

    def _extract_technical_terms(self) -> None:
        """Extract technical terms and acronyms"""
        tech_terms = re.findall(r'\b[A-Z]{2,6}\b', self.job_description)

        non_technical = {
            'the', 'and', 'for', 'you', 'are', 'our',
            'inc', 'llc', 'corp', 'ltd'
        }

        for term in tech_terms:
            term_lower = term.lower()
            if term_lower not in non_technical:
                if term_lower not in self.keyword_scores:
                    self.keyword_scores[term_lower] = 0
                self.keyword_scores[term_lower] += 1

    def _extract_requirement_phrases(self) -> None:
        """Extract keywords from requirement phrases"""
        requirement_patterns = [
            r'(?:required|must have|experience with|proficient in|knowledge of|familiar with|expertise in)\s+([^.!?\n]+)',
            r'(?:skills in|background in|strong|solid|deep understanding of|experience in)\s+([^.!?\n]+)',
            r'(?:proficiency|proficient|expert|advanced|intermediate) (?:in|with|knowledge of)\s+([^.!?\n]+)'
        ]

        for pattern in requirement_patterns:
            matches = re.findall(pattern, self.text_lower, re.IGNORECASE)
            for match in matches:
                terms = re.findall(r'\b[a-z]+(?:[.\-/][a-z]+)*\b', match)
                for term in terms:
                    if len(term) > 2:
                        if term not in self.keyword_scores:
                            self.keyword_scores[term] = 0
                        self.keyword_scores[term] += 3  # Higher weight

    def _extract_tech_stack(self) -> None:
        """Extract technology stack keywords"""
        tech_stack_patterns = [
            r'(?:tech stack|technology stack|technologies|tools|frameworks?):\s*([^.!?\n]+)',
            r'(?:using|working with|built with):\s*([^.!?\n]+)'
        ]

        for pattern in tech_stack_patterns:
            matches = re.findall(pattern, self.text_lower, re.IGNORECASE)
            for match in matches:
                terms = re.findall(r'\b[a-z]+(?:[.\-/][a-z]+)*\b', match)
                for term in terms:
                    if len(term) > 2:
                        if term not in self.keyword_scores:
                            self.keyword_scores[term] = 0
                        self.keyword_scores[term] += 2

    def _filter_keywords(self) -> List[str]:
        """Filter out stop words and low-scoring keywords"""
        return [
            kw for kw, score in self.keyword_scores.items()
            if kw.lower() not in STOP_WORDS and len(kw) > 2 and score > 0
        ]


def extract_keywords_from_job_description(job_description: str) -> List[str]:
    """
    Extract relevant keywords from job description

    Args:
        job_description: Job description text

    Returns:
        List of extracted keywords sorted by relevance
    """
    extractor = KeywordExtractor(job_description)
    return extractor.extract()
