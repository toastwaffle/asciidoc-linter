# rules.py - Base classes for linting rules
"""
Base classes and interfaces for AsciiDoc linting rules
"""

from .rules.base import Severity, Position, Finding, Rule, RuleRegistry

__all__ = ['Severity', 'Position', 'Finding', 'Rule', 'RuleRegistry']