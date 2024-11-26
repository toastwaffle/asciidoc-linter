# base.py - Base functionality for rules
"""
Base functionality and registry for AsciiDoc linting rules
"""

from typing import Type, Dict, List
from ..rules import Rule

class RuleRegistry:
    """Registry for all available rules"""
    
    _rules: Dict[str, Type[Rule]] = {}
    
    @classmethod
    def register_rule(cls, rule_class: Type[Rule]):
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