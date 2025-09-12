"""
SOLAR EMERGENCE - Constraint Enforcement Layer
This agent ensures ALL processed knowledge adheres to project constraints
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import re
import hashlib

class ConstraintViolation(Enum):
    """Types of constraint violations to detect and correct"""
    CLOUD_DEPENDENCY = "cloud_dependency"
    PAID_SERVICE = "paid_service"
    EXTERNAL_API = "external_api"
    PREDETERMINED_PATTERN = "predetermined_pattern"
    NON_LOCAL = "non_local"
    NON_EMERGENT = "non_emergent"

@dataclass
class ProjectConstraints:
    """
    IMMUTABLE CORE CONSTRAINTS FOR SOLAR EMERGENCE
    These NEVER change regardless of input
    """
    
    # FUNDAMENTAL PRINCIPLES
    core_principles = [
        "DISCOVERY_FIRST: Let mathematics reveal patterns, don't dictate them",
        "LOCAL_ONLY: Everything runs on Mac M2 Max, no cloud",
        "ZERO_COST: No paid APIs, services, or subscriptions",
        "EMERGENT: Patterns emerge from data, not from rules",
        "SEQUENTIAL: Each video builds on previous intelligence",
        "MULTIMODAL: All signals matter equally until proven otherwise"
    ]
    
    # TECHNICAL CONSTRAINTS
    technical_requirements = {
        "hardware": "Mac M2 Max local execution",
        "apis": "NO external APIs except localhost bridges",
        "storage": "Local filesystem and Docker containers only",
        "ml_models": "Local models only (MLX, local Whisper, etc)",
        "internet": "Only for downloading models/data, not runtime",
        "cost": "Zero recurring costs"
    }

class ConstraintEnforcer:
    """Enforces project constraints on all knowledge artifacts"""
    
    def __init__(self):
        self.constraints = ProjectConstraints()
        self.violation_patterns = self._build_violation_patterns()
    
    def _build_violation_patterns(self) -> Dict[ConstraintViolation, List[str]]:
        """Build regex patterns to detect constraint violations"""
        return {
            ConstraintViolation.CLOUD_DEPENDENCY: [
                r'aws\.|azure\.|gcp\.|google cloud',
                r'firebase|s3 bucket|ec2|lambda',
                r'cloud\s+deployment|cloud\s+storage'
            ],
            ConstraintViolation.PAID_SERVICE: [
                r'openai api|anthropic api|cohere api',
                r'\$\d+/month|\$\d+/year|subscription',
                r'premium|paid tier|commercial license'
            ],
            ConstraintViolation.EXTERNAL_API: [
                r'api\..*\.com|https://api\.',
                r'fetch\(.*api|requests\.get.*api',
                r'curl.*api|wget.*api'
            ],
            ConstraintViolation.PREDETERMINED_PATTERN: [
                r'must use|should follow|required pattern',
                r'template|boilerplate|standard approach',
                r'best practice.*must|convention.*required'
            ]
        }
    
    def scan_content(self, content: str, source: str) -> Dict[str, Any]:
        """Scan content for constraint violations"""
        violations = []
        
        for violation_type, patterns in self.violation_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    violations.append({
                        'type': violation_type.value,
                        'pattern': pattern,
                        'match': match.group(),
                        'position': match.span(),
                        'context': self._get_context(content, match.span())
                    })
        
        return {
            'source': source,
            'violations': violations,
            'is_compliant': len(violations) == 0,
            'content_hash': hashlib.sha256(content.encode()).hexdigest()[:8]
        }
    
    def _get_context(self, content: str, span: tuple, context_size: int = 100) -> str:
        """Get surrounding context for a violation"""
        start, end = span
        context_start = max(0, start - context_size)
        context_end = min(len(content), end + context_size)
        return content[context_start:context_end]
    
    def generate_compliant_alternative(self, violation: Dict[str, Any]) -> str:
        """Generate constraint-compliant alternative for violation"""
        violation_type = ConstraintViolation(violation['type'])
        
        alternatives = {
            ConstraintViolation.CLOUD_DEPENDENCY: "Use local Docker containers or filesystem",
            ConstraintViolation.PAID_SERVICE: "Use local/open-source alternatives",
            ConstraintViolation.EXTERNAL_API: "Create local bridge or use offline data",
            ConstraintViolation.PREDETERMINED_PATTERN: "Let patterns emerge from data analysis"
        }
        
        return alternatives.get(violation_type, "Review against project constraints")
    
    def enforce_constraints(self, content: str, source: str) -> Dict[str, Any]:
        """Main constraint enforcement pipeline"""
        scan_result = self.scan_content(content, source)
        
        if not scan_result['is_compliant']:
            # Generate alternatives for each violation
            for violation in scan_result['violations']:
                violation['alternative'] = self.generate_compliant_alternative(violation)
        
        return {
            'original_source': source,
            'scan_result': scan_result,
            'enforcement_timestamp': hashlib.sha256(f"{source}{content}".encode()).hexdigest()[:16],
            'constraints_version': "1.0.0"
        }

if __name__ == "__main__":
    # Example usage
    enforcer = ConstraintEnforcer()
    
    test_content = """
    To implement this feature, you should use the OpenAI API
    and deploy it on AWS with Firebase authentication.
    """
    
    result = enforcer.enforce_constraints(test_content, "test_article.md")
    print(f"Compliant: {result['scan_result']['is_compliant']}")
    for violation in result['scan_result']['violations']:
        print(f"Violation: {violation['type']} - {violation['alternative']}")
