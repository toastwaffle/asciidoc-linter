# linter.py - Main linter module
"""
Main linter module that processes AsciiDoc files and applies rules
"""

from typing import List, Optional
from pathlib import Path

from .rules.heading_rules import (
    HeadingFormatRule,
    HeadingHierarchyRule,
    MultipleTopLevelHeadingsRule
)
from .rules.block_rules import (
    UnterminatedBlockRule,
    BlockSpacingRule
)
from .rules.whitespace_rules import WhitespaceRule
from .rules.image_rules import ImageAttributesRule
from .parser import AsciiDocParser
from .reporter import LintReport, LintError, ConsoleReporter, Reporter

class AsciiDocLinter:
    """Main linter class that coordinates parsing and rule checking"""
    
    def __init__(self):
        self.parser = AsciiDocParser()
        self.rules = [
            HeadingFormatRule(),
            HeadingHierarchyRule(),
            MultipleTopLevelHeadingsRule(),
            UnterminatedBlockRule(),
            BlockSpacingRule(),
            WhitespaceRule(),
            ImageAttributesRule()
        ]
        self.reporter = ConsoleReporter()  # Default reporter
    
    def set_reporter(self, reporter: Reporter) -> None:
        """Set the reporter to use for output formatting"""
        self.reporter = reporter
    
    def lint(self, content: str, source: Optional[str] = None) -> str:
        """
        Lint content and return formatted output using the current reporter
        
        This is the main entry point used by the CLI
        """
        report = self.lint_string(content, source)
        return self.reporter.format_report(report)
    
    def lint_file(self, file_path: Path) -> LintReport:
        """Lint a single file and return a report"""
        try:
            content = file_path.read_text()
            return self.lint_string(content, str(file_path))
        except Exception as e:
            return LintReport([LintError(str(file_path), 0, f"Error reading file: {e}")])
    
    def lint_string(self, content: str, source: Optional[str] = None) -> LintReport:
        """Lint a string and return a report"""
        document = self.parser.parse(content)
        errors = []
        
        for rule in self.rules:
            rule_errors = rule.check(document)
            errors.extend(rule_errors)
        
        if source:
            for error in errors:
                error.file = source
        
        return LintReport(errors)