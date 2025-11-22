"""
Local LLM Provider Implementation
Compatible with OpenAI API format (e.g., LM Studio)
"""

import json
from typing import Dict, Any

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

from .base import AIProvider, AIProviderError


class LocalLLMProvider(AIProvider):
    """Local LLM provider implementation (OpenAI-compatible)"""

    def __init__(self, base_url: str, model: str = "local-model"):
        """
        Initialize Local LLM provider

        Args:
            base_url: Base URL of local LLM server
            model: Model name

        Raises:
            AIProviderError: If OpenAI package not available
        """
        if not OPENAI_AVAILABLE:
            raise AIProviderError(
                "OpenAI package not available. Install with: pip install openai"
            )

        self.client = OpenAI(
            api_key="not-needed",  # Local LLM doesn't require real API key
            base_url=base_url,
        )
        self._model_name = model
        self._base_url = base_url

    @property
    def provider_name(self) -> str:
        return "local"

    @property
    def model_name(self) -> str:
        return self._model_name

    def parse_resume_text(self, text_resume: str) -> Dict[str, Any]:
        """Convert text resume to structured JSON using local LLM"""
        if not text_resume or not text_resume.strip():
            raise ValueError("Text resume cannot be empty")

        system_prompt = self._get_parsing_system_prompt()
        user_prompt = f"Convert this resume to JSON:\n\n{text_resume}"

        try:
            response = self.client.chat.completions.create(
                model=self._model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=4000,
            )

            json_content = self._extract_json_from_response(response)
            parsed_resume = json.loads(json_content)

            return parsed_resume

        except json.JSONDecodeError as e:
            raise AIProviderError(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            raise AIProviderError(f"Local LLM parsing failed: {str(e)}")

    def test_connectivity(self) -> Dict[str, Any]:
        """Test local LLM connectivity"""
        try:
            response = self.client.chat.completions.create(
                model=self._model_name,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
            )
            return {
                "success": True,
                "provider": self.provider_name,
                "model": self.model_name,
                "base_url": self._base_url,
            }
        except Exception as e:
            return {
                "success": False,
                "provider": self.provider_name,
                "model": self.model_name,
                "base_url": self._base_url,
                "error": str(e),
            }

    def _extract_json_from_response(self, response) -> str:
        """Extract and clean JSON from AI response"""
        json_content = response.choices[0].message.content.strip()

        # Remove markdown formatting if present
        if json_content.startswith("```json"):
            json_content = json_content[7:]
        if json_content.endswith("```"):
            json_content = json_content[:-3]

        return json_content.strip()

    def _get_parsing_system_prompt(self) -> str:
        """Get the system prompt for resume parsing"""
        # Use same prompt as OpenAI for consistency
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
    }
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
      "description": "Project description",
      "keywords": ["relevant", "keywords"],
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

Return ONLY the JSON structure, no additional text."""
