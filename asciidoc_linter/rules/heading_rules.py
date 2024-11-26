# heading_rules.py - Rules for checking AsciiDoc headings

import re
from typing import List, Dict, Any
from .base_rules import Rule, Finding, Severity, Position

class HeadingHierarchyRule(Rule):
    """Rule to check if heading levels are properly nested"""
    rule_id = "HDR001"
    
    def check(self, content: str) -> List[Finding]:
        findings = []
        current_level = 0
        for line_num, line in enumerate(content.split('\n'), 1):
            if line.startswith('='):
                level = len(re.match(r'^=+', line).group())
                if level > current_level + 1:
                    findings.append(Finding(
                        message=f"Heading level skipped. Found level {level} after level {current_level}",
                        severity=Severity.ERROR,
                        position=Position(line=line_num),
                        rule_id=self.rule_id,
                        context={"current_level": current_level, "found_level": level}
                    ))
                current_level = level
        return findings

class HeadingFormatRule(Rule):
    """Rule to check if headings follow the correct format"""
    rule_id = "HDR002"
    
    def check(self, content: str) -> List[Finding]:
        findings = []
        for line_num, line in enumerate(content.split('\n'), 1):
            if line.startswith('='):
                # Get the heading level and remaining text
                equals_part = re.match(r'^=+', line).group()
                remaining_text = line[len(equals_part):]
                
                context = {
                    "line": line,
                    "level": len(equals_part),
                    "text": remaining_text.strip()
                }
                
                # Check 1: Space after equals signs
                if not remaining_text.startswith(' '):
                    findings.append(Finding(
                        message=f"No space after {'=' * len(equals_part)} signs",
                        severity=Severity.ERROR,
                        position=Position(line=line_num),
                        rule_id=self.rule_id,
                        context=context
                    ))
                
                # Check 2: Capitalization of heading text
                text = remaining_text.strip()
                if text and not text[0].isupper():
                    findings.append(Finding(
                        message="Heading text must start with capital letter",
                        severity=Severity.ERROR,
                        position=Position(line=line_num),
                        rule_id=self.rule_id,
                        context=context
                    ))
        
        return findings

class HeadingIncrementationRule(Rule):
    """Rule to check if heading levels are incremented properly"""
    rule_id = "HDR003"
    
    def check(self, content: str) -> List[Finding]:
        findings = []
        current_level = 0
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.startswith('='):
                level = len(re.match(r'^=+', line).group())
                
                # Skip if it's a heading underline
                if line_num > 1 and lines[line_num - 2].strip() and not lines[line_num - 2].startswith('='):
                    continue
                    
                if level > current_level + 1:
                    findings.append(Finding(
                        message=f"Heading level incremented by more than one. Found level {level} after level {current_level}",
                        severity=Severity.ERROR,
                        position=Position(line=line_num),
                        rule_id=self.rule_id,
                        context={
                            "current_level": current_level,
                            "found_level": level,
                            "line": line
                        }
                    ))
                current_level = level
                
        return findings

class MultipleTopLevelHeadingsRule(Rule):
    """Rule to check if there are multiple top-level headings"""
    rule_id = "HDR004"
    
    def check(self, content: str) -> List[Finding]:
        findings = []
        top_level_headings = []
        
        for line_num, line in enumerate(content.split('\n'), 1):
            if line.startswith('=') and not line.startswith('=='):
                # Found a top-level heading
                heading_text = line.lstrip('= ').strip()
                top_level_headings.append((line_num, heading_text))
        
        # If we found more than one top-level heading
        if len(top_level_headings) > 1:
            # Create a finding for each additional top-level heading
            for line_num, heading_text in top_level_headings[1:]:
                findings.append(Finding(
                    message="Multiple top-level headings found. Only one is allowed.",
                    severity=Severity.ERROR,
                    position=Position(line=line_num),
                    rule_id=self.rule_id,
                    context={
                        "first_heading": top_level_headings[0][1],
                        "first_heading_line": top_level_headings[0][0],
                        "current_heading": heading_text
                    }
                ))
        
        return findings