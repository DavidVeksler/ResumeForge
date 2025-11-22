"""
Validation models
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ValidationResult:
    """Container for validation results"""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)"""
        return len(self.errors) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "recommendations": self.recommendations if self.is_valid else [],
        }
