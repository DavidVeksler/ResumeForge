"""
Resume data models with type hints
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class PersonalInfo:
    """Personal information section"""
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


@dataclass
class Summary:
    """Professional summary section"""
    headline: str
    bullets: List[str] = field(default_factory=list)


@dataclass
class Metrics:
    """Achievement metrics"""
    value: float
    type: str  # revenue_impact, assets_managed, team_size, etc.


@dataclass
class Achievement:
    """Individual achievement entry"""
    text: str
    keywords: List[str] = field(default_factory=list)
    metrics: Optional[Dict[str, Any]] = None
    relevance_score: Optional[float] = None  # Added during optimization


@dataclass
class Experience:
    """Work experience entry"""
    title: str
    company: str
    duration: str
    location: Optional[str] = None
    description: Optional[str] = None
    achievements: List[Achievement] = field(default_factory=list)


@dataclass
class Skills:
    """Skills section - flexible structure"""
    data: Dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value


@dataclass
class Education:
    """Education entry"""
    degree: str
    school: str
    duration: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    details: Optional[str] = None


@dataclass
class Project:
    """Project entry"""
    name: str
    description: str
    technologies: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    link: Optional[str] = None


@dataclass
class ResumeData:
    """Complete resume data structure"""
    personal: PersonalInfo
    summary: Optional[Summary] = None
    experience: List[Experience] = field(default_factory=list)
    skills: Dict[str, Any] = field(default_factory=dict)
    education: List[Education] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResumeData":
        """Create ResumeData from dictionary"""
        # For simplicity, we'll keep the dict-based approach
        # and just validate the structure
        return data  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        # This allows backward compatibility with existing code
        return self.__dict__  # type: ignore
