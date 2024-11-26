# rules.py - Base classes for linting rules
"""
Base classes and interfaces for AsciiDoc linting rules
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Severity(Enum):
    """Severity levels for lint findings"""
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'

@dataclass
class Position:
    """Position in a file"""
    line: int
    column: Optional[int] = None

@dataclass
class Finding:
    """A lint finding"""
    rule_id: str
    message: str
    severity: Severity
    position: Position
    context: Optional[str] = None

class Rule(ABC):
    """Base class for all linting rules"""
    
    def __init__(self):
        self.id = self.__class__.__name__
        
    @abstractmethod
    def check(self, content: str) -> List[Finding]:
        """Check content and return findings"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what this rule checks"""
        pass