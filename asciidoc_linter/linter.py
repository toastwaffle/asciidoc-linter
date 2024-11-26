# linter.py - Main linter class
"""
Main linter class that coordinates rule checking and reporting
"""

from typing import List, Type
from .rules import Rule, Finding
from .heading_rules import HeadingIncrementationRule
from .reporter import Reporter, ConsoleReporter, JsonReporter, HtmlReporter

class AsciiDocLinter:
    """Main linter class"""
    
    def __init__(self):
        self.rules: List[Rule] = []
        self.reporter: Reporter = ConsoleReporter()
        
        # Register default rules
        self.register_rule(HeadingIncrementationRule())
    
    def register_rule(self, rule: Rule) -> None:
        """Register a new rule"""
        self.rules.append(rule)
    
    def set_reporter(self, reporter: Reporter) -> None:
        """Set the reporter to use"""
        self.reporter = reporter
    
    def lint(self, content: str) -> str:
        """
        Lint the given content and return the formatted results
        
        Args:
            content: The AsciiDoc content to lint
            
        Returns:
            Formatted lint results as string
        """
        all_findings: List[Finding] = []
        
        # Apply each rule
        for rule in self.rules:
            findings = rule.check(content)
            all_findings.extend(findings)
        
        # Sort findings by line number
        all_findings.sort(key=lambda f: f.position.line)
        
        # Format and return results
        return self.reporter.report(all_findings)