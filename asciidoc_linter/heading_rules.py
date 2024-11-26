# heading_rules.py - Implementation of heading rules
"""
This module contains rules for checking AsciiDoc heading structure and format.
"""

from typing import List, Optional, Tuple
from .rules import Rule, Finding, Severity, Position

class HeadingFormatRule(Rule):
    """
    HEAD002: Check heading format.
    Ensures that headings follow AsciiDoc conventions:
    - Space after = characters
    - Proper capitalization
    """
    
    def __init__(self):
        super().__init__()
        self.id = "HEAD002"
    
    @property
    def description(self) -> str:
        return "Ensures proper heading format (spacing and capitalization)"
    
    def check(self, content: str) -> List[Finding]:
        findings = []
        
        for line_num, line in enumerate(content.splitlines(), 1):
            # Skip empty lines and non-heading lines
            if not line or not line.startswith('='):
                continue
            
            # Skip lines that look like header underlines (====)
            if line.strip() == '=' * len(line.strip()):
                continue
            
            # Count leading = characters
            level = 0
            for char in line:
                if char != '=':
                    break
                level += 1
            
            # Get the heading text, handling both cases:
            # 1. No space after = (=Title)
            # 2. Space after = (= Title)
            heading_text = line[level:].strip()
            
            # Check for space after = characters
            if level > 0 and (len(line) <= level or line[level] != ' '):
                findings.append(Finding(
                    rule_id=self.id,
                    message=f"Missing space after {'=' * level}",
                    severity=Severity.ERROR,
                    position=Position(line=line_num),
                    context=line.strip()
                ))
            
            # Check if heading starts with lowercase (only if we have text)
            if heading_text:
                # Split into words and check first word
                words = heading_text.split()
                if words and words[0][0].islower():
                    findings.append(Finding(
                        rule_id=self.id,
                        message="Heading should start with uppercase letter",
                        severity=Severity.WARNING,
                        position=Position(line=line_num),
                        context=line.strip()
                    ))
        
        return findings

class HeadingIncrementationRule(Rule):
    """
    HEAD001: Check for proper heading incrementation.
    Ensures that heading levels are not skipped (e.g., h1 -> h3).
    """
    
    def __init__(self):
        super().__init__()
        self.id = "HEAD001"
    
    @property
    def description(self) -> str:
        return "Ensures proper heading level incrementation (no skipped levels)"
    
    def check(self, content: str) -> List[Finding]:
        findings = []
        current_level = 0
        last_heading_line = 0
        
        for line_num, line in enumerate(content.splitlines(), 1):
            # Skip empty lines and non-heading lines
            if not line or not line.startswith('='):
                continue
            
            # Count the number of '=' at the start of the line
            level = 0
            for char in line:
                if char != '=':
                    break
                level += 1
            
            # Skip lines that look like header underlines (====)
            if level == len(line.strip()):
                continue
                
            # First heading can be any level
            if current_level == 0:
                current_level = level
                last_heading_line = line_num
                continue
            
            # Check if we're skipping levels
            if level > current_level + 1:
                findings.append(Finding(
                    rule_id=self.id,
                    message=f"Heading level skipped: found h{level} after h{current_level}",
                    severity=Severity.ERROR,
                    position=Position(line=line_num),
                    context=line.strip()
                ))
            
            current_level = level
            last_heading_line = line_num
            
        return findings

class MultipleTopLevelHeadingsRule(Rule):
    """
    HEAD003: Check for multiple top-level headings.
    Ensures that a document has only one top-level (=) heading.
    """
    
    def __init__(self):
        super().__init__()
        self.id = "HEAD003"
    
    @property
    def description(self) -> str:
        return "Ensures document has only one top-level heading"
    
    def check(self, content: str) -> List[Finding]:
        findings = []
        first_top_level: Optional[Tuple[int, str]] = None  # (line_number, heading_text)
        
        for line_num, line in enumerate(content.splitlines(), 1):
            # Skip empty lines and non-heading lines
            if not line or not line.startswith('='):
                continue
            
            # Skip lines that look like header underlines (====)
            if line.strip() == '=' * len(line.strip()):
                continue
            
            # Count leading = characters
            level = 0
            for char in line:
                if char != '=':
                    break
                level += 1
            
            # Check for top-level headings (single =)
            if level == 1:
                heading_text = line[level:].strip()
                
                if first_top_level is None:
                    # Remember first top-level heading
                    first_top_level = (line_num, heading_text)
                else:
                    # Found another top-level heading
                    findings.append(Finding(
                        rule_id=self.id,
                        message=f"Multiple top-level headings found. First heading at line {first_top_level[0]}: '{first_top_level[1]}'",
                        severity=Severity.ERROR,
                        position=Position(line=line_num),
                        context=line.strip()
                    ))
        
        return findings