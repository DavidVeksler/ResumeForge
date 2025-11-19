"""
AI Service - Handles AI provider configuration and text-to-JSON conversion
"""

import json
import os
from typing import Dict, Any

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


class AIProviderError(Exception):
    """Raised when AI provider is not available or misconfigured"""
    pass


class AIService:
    """Service for managing AI provider interactions"""

    def __init__(self):
        """Initialize AI service with environment configuration"""
        if not OPENAI_AVAILABLE:
            raise AIProviderError("OpenAI package not available. Install with: pip install openai")

        self.provider = os.getenv('AI_PROVIDER', 'local').lower()
        self.client = self._initialize_client()
        self.model_name = self._get_model_name()

    def _initialize_client(self) -> OpenAI:
        """Initialize the appropriate AI client based on configuration"""
        if self.provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise AIProviderError(
                    'OpenAI API key not configured. Set OPENAI_API_KEY environment variable.'
                )
            return OpenAI(api_key=api_key)
        else:
            # Local LLM configuration (default)
            base_url = os.getenv('LOCAL_LLM_BASE_URL', 'http://172.28.144.1:1234/v1')
            return OpenAI(
                api_key="local-key",  # Local LLM doesn't require real API key
                base_url=base_url
            )

    def _get_model_name(self) -> str:
        """Get the model name based on provider"""
        if self.provider == 'openai':
            return os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        else:
            return os.getenv('LOCAL_MODEL_NAME', 'local-model')

    def parse_resume_text(self, text_resume: str) -> Dict[str, Any]:
        """
        Convert text resume to structured JSON format

        Args:
            text_resume: Raw text resume content

        Returns:
            Parsed resume data as dictionary

        Raises:
            AIProviderError: If parsing fails
            ValueError: If input is invalid
        """
        if not text_resume or not text_resume.strip():
            raise ValueError("Text resume cannot be empty")

        system_prompt = self._get_parsing_system_prompt()
        user_prompt = f"Convert this resume to JSON:\n\n{text_resume}"

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent formatting
                max_tokens=4000
            )

            json_content = self._extract_json_from_response(response)
            parsed_resume = json.loads(json_content)

            return parsed_resume

        except json.JSONDecodeError as e:
            raise AIProviderError(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            raise AIProviderError(f"Resume parsing failed: {str(e)}")

    def _extract_json_from_response(self, response) -> str:
        """Extract and clean JSON from AI response"""
        json_content = response.choices[0].message.content.strip()

        # Remove markdown formatting if present
        if json_content.startswith('```json'):
            json_content = json_content[7:]
        if json_content.endswith('```'):
            json_content = json_content[:-3]

        return json_content.strip()

    def _get_parsing_system_prompt(self) -> str:
        """Get the system prompt for resume parsing"""
        return """You are a resume parsing expert. Convert the provided text resume into a structured JSON format exactly matching this schema:

{
  "personal": {
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+1 (555) 123-4567",
    "location": "City, State",
    "linkedin": "linkedin.com/in/profile"
  },
  "summary": {
    "headline": "Professional headline/summary",
    "bullets": ["Key strength 1", "Key strength 2", "Key strength 3"]
  },
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State",
      "duration": "Start Date - End Date",
      "description": "Brief role description",
      "achievements": [
        {
          "text": "Achievement description with specific metrics",
          "keywords": ["relevant", "keywords", "for", "ats"],
          "metrics": {"value": 100000, "type": "revenue_impact"}
        }
      ]
    }
  ],
  "skills": {
    "programming_languages": {
      "expert": ["Language1", "Language2"],
      "proficient": ["Language3", "Language4"],
      "familiar": ["Language5"]
    },
    "web_technologies": {
      "expert": ["Framework1"],
      "proficient": ["Framework2", "Framework3"]
    },
    "fintech": ["blockchain", "defi", "payments"],
    "leadership": ["team management", "project leadership"]
  },
  "education": [
    {
      "degree": "Degree Name",
      "school": "University Name",
      "duration": "Start - End Year",
      "description": "Relevant details or achievements"
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "description": "Project description highlighting impact",
      "keywords": ["relevant", "technical", "keywords"],
      "achievements": ["Key outcome 1", "Key outcome 2"]
    }
  ]
}

Instructions:
1. Extract ALL information accurately from the text
2. For achievements, identify quantifiable metrics and convert to numbers
3. Add relevant ATS keywords based on the role/industry context
4. Organize skills by proficiency level and category
5. If information is missing, use reasonable defaults or omit optional fields
6. Ensure all JSON is valid and properly formatted
7. Focus on FinTech/technology keywords when applicable

Return ONLY the JSON structure, no additional text."""

    def test_connectivity(self) -> Dict[str, Any]:
        """
        Test AI provider connectivity

        Returns:
            Dictionary with test results
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return {
                'success': True,
                'provider': self.provider,
                'model': self.model_name
            }
        except Exception as e:
            return {
                'success': False,
                'provider': self.provider,
                'model': self.model_name,
                'error': str(e)
            }
