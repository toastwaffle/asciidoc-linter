# base_rules.py - Contains base classes for the rule system

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class Position:
    line: int
    column: Optional[int] = None

@dataclass
class Finding:
    message: str
    severity: Severity
    position: Position
    rule_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class Rule:
    """Base class for all rules"""
    rule_id: str = "BASE"  # Should be overridden by subclasses
    
    def check(self, content: str) -> List[Finding]:
        """
        Check the content for rule violations
        
        Args:
            content: The content to check
            
        Returns:
            List of findings
        """
        raise NotImplementedError("Rule must implement check method")