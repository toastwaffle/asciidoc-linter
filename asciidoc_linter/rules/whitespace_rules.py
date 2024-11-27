# whitespace_rules.py - Rules for checking whitespace in AsciiDoc files

from typing import List
from .base import Rule, Finding, Severity, Position

class WhitespaceRule(Rule):
    """Rule to check for proper whitespace usage."""
    
    id = "WS001"
    name = "Whitespace Check"
    description = "Checks for proper whitespace usage"
    severity = Severity.WARNING

    def __init__(self):
        super().__init__()
        self.consecutive_empty_lines = 0

    def check_line(self, line: str, line_number: int, context: List[str]) -> List[Finding]:
        findings = []
        
        # Check for multiple consecutive empty lines
        if not line.strip():
            self.consecutive_empty_lines += 1
            if self.consecutive_empty_lines > 2:
                findings.append(
                    Finding(
                        rule_id=self.id,
                        position=Position(line=line_number + 1),
                        message="Too many consecutive empty lines",
                        severity=self.severity,
                        context=line
                    )
                )
        else:
            self.consecutive_empty_lines = 0
        
        # Check for proper list marker spacing
        if line.lstrip().startswith(('*', '-', '.')):
            marker = line.lstrip()[0]
            indent = len(line) - len(line.lstrip())
            content = line.lstrip()[1:]
            
            if not content.startswith(' '):
                findings.append(
                    Finding(
                        rule_id=self.id,
                        position=Position(line=line_number + 1),
                        message=f"Missing space after the marker '{marker}'",
                        severity=self.severity,
                        context=line
                    )
                )
        
        # Check for trailing whitespace
        if line.rstrip() != line:
            findings.append(
                Finding(
                    rule_id=self.id,
                    position=Position(line=line_number + 1),
                    message="Line contains trailing whitespace",
                    severity=self.severity,
                    context=line
                )
            )
        
        # Check for tabs
        if '\t' in line:
            findings.append(
                Finding(
                    rule_id=self.id,
                    position=Position(line=line_number + 1),
                    message="Line contains tabs (use spaces instead)",
                    severity=self.severity,
                    context=line
                )
            )
        
        # Check for proper section title spacing
        if line.startswith('='):
            # Count leading = characters
            level = 0
            for char in line:
                if char != '=':
                    break
                level += 1
            
            # Check spacing after = characters
            if len(line) > level and line[level] != ' ':
                findings.append(
                    Finding(
                        rule_id=self.id,
                        position=Position(line=line_number + 1),
                        message=f"Missing space after {'=' * level}",
                        severity=self.severity,
                        context=line
                    )
                )
            
            # Check for blank line before section title (except for first line)
            if line_number > 0 and context[line_number - 1].strip():
                findings.append(
                    Finding(
                        rule_id=self.id,
                        position=Position(line=line_number + 1),
                        message="Section title should be preceded by a blank line",
                        severity=self.severity,
                        context=line
                    )
                )
            
            # Check for blank line after section title (except for last line)
            if line_number < len(context) - 1 and context[line_number + 1].strip():
                findings.append(
                    Finding(
                        rule_id=self.id,
                        position=Position(line=line_number + 1),
                        message="Section title should be followed by a blank line",
                        severity=self.severity,
                        context=line
                    )
                )
        
        # Check for proper admonition block spacing
        admonition_markers = ['NOTE:', 'TIP:', 'IMPORTANT:', 'WARNING:', 'CAUTION:']
        if any(line.strip().startswith(marker) for marker in admonition_markers):
            if line_number > 0 and context[line_number - 1].strip():
                findings.append(
                    Finding(
                        rule_id=self.id,
                        position=Position(line=line_number + 1),
                        message="Admonition block should be preceded by a blank line",
                        severity=self.severity,
                        context=line
                    )
                )
        
        return findings