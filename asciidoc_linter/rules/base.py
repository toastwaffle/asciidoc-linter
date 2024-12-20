# base.py - Base functionality for rules
"""
Base functionality and registry for AsciiDoc linting rules.
This module provides the core classes and functionality for the rule system.
"""

from typing import Type, Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class Severity(Enum):
    """Severity levels for findings"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    
    def __str__(self) -> str:
        return self.value

@dataclass
class Position:
    """Represents a position in a text file"""
    line: int
    column: Optional[int] = None
    
    def __str__(self) -> str:
        if self.column is not None:
            return f"line {self.line}, column {self.column}"
        return f"line {self.line}"

@dataclass
class Finding:
    """Represents a rule violation finding"""
    message: str
    severity: Severity
    position: Position
    rule_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    
    @property
    def line_number(self) -> int:
        """Backward compatibility for line number access"""
        return self.position.line

class Rule:
    """Base class for all rules"""
    id: str = "BASE"  # Default ID, should be overridden by subclasses
    name: str = ""  # Should be overridden by subclasses
    description: str = ""  # Should be overridden by subclasses
    severity: Severity = Severity.WARNING  # Default severity
    
    @property
    def rule_id(self) -> str:
        """
        Returns the rule ID. This is a compatibility property that returns
        the same value as the id attribute.
        """
        return self.id
    
    def check(self, content: str) -> List[Finding]:
        """
        Check the content for rule violations.
        Must be implemented by concrete rule classes.
        
        Args:
            content: The content to check
            
        Returns:
            List of findings
        """
        raise NotImplementedError("Rule must implement check method")
    
    def check_line(self, line: str, line_number: int, context: List[str]) -> List[Finding]:
        """
        Check a single line for rule violations.
        
        Args:
            line: The current line to check
            line_number: The line number in the document (0-based)
            context: The complete document as a list of lines
            
        Returns:
            List of Finding objects representing rule violations
        """
        findings = []
        
        # Get previous and next lines if available
        prev_line = context[line_number - 1] if line_number > 0 else None
        next_line = context[line_number + 1] if line_number < len(context) - 1 else None
        
        # Check the line content
        line_findings = self.check_line_content(line, line_number)
        if line_findings:
            findings.extend(line_findings)
            
        # Check line context if needed
        context_findings = self.check_line_context(line, line_number, prev_line, next_line)
        if context_findings:
            findings.extend(context_findings)
            
        return findings
    
    def check_line_content(self, line: str, line_number: int) -> List[Finding]:
        """
        Check the content of a single line.
        Override this method in concrete rule implementations.
        """
        return []
    
    def check_line_context(self, line: str, line_number: int, 
                          prev_line: Optional[str], next_line: Optional[str]) -> List[Finding]:
        """
        Check a line in context with its surrounding lines.
        Override this method in concrete rule implementations.
        """
        return []
    
    def create_finding(self, line_number: int, message: str, 
                      column: Optional[int] = None, context: Optional[Dict[str, Any]] = None) -> Finding:
        """Helper method to create a Finding object"""
        return Finding(
            message=message,
            severity=self.severity,
            position=Position(line=line_number, column=column),
            rule_id=self.rule_id,
            context=context
        )

class RuleRegistry:
    """Registry for all available rules"""
    
    _rules: Dict[str, Type[Rule]] = {}
    
    @classmethod
    def register_rule(cls, rule_class: Type[Rule]) -> None:
        """Register a new rule class"""
        cls._rules[rule_class.__name__] = rule_class
    
    @classmethod
    def get_rule(cls, rule_name: str) -> Type[Rule]:
        """Get a rule class by name"""
        return cls._rules[rule_name]
    
    @classmethod
    def get_all_rules(cls) -> List[Type[Rule]]:
        """Get all registered rules"""
        return list(cls._rules.values())
    
    @classmethod
    def create_all_rules(cls) -> List[Rule]:
        """Create instances of all registered rules"""
        return [rule_class() for rule_class in cls.get_all_rules()]