# block_rules.py - Rules for checking AsciiDoc blocks

from typing import List, Dict
from .base import Rule, Finding, Severity, Position

class UnterminatedBlockRule(Rule):
    """Rule to check for unterminated blocks in AsciiDoc files."""
    
    id = "BLOCK001"
    name = "Unterminated Block Check"
    description = "Checks for blocks that are not properly terminated"
    severity = Severity.ERROR

    def __init__(self):
        super().__init__()
        self.block_markers = {
            "----": "listing block",
            "====": "example block",
            "****": "sidebar block",
            "....": "literal block",
            "____": "quote block",
            "|===": "table block",
            "////": "comment block",
            "++++": "passthrough block",
        }
        self.open_blocks: Dict[str, int] = {}

    def check_line(self, line: str, line_number: int, context: List[str]) -> List[Finding]:
        findings = []
        stripped_line = line.strip()
        
        # Check if line is a block delimiter
        if stripped_line in self.block_markers:
            if stripped_line in self.open_blocks:
                # This is a closing delimiter
                del self.open_blocks[stripped_line]
            else:
                # This is an opening delimiter
                self.open_blocks[stripped_line] = line_number
                
                # Look ahead for matching end delimiter
                is_terminated = False
                for i, next_line in enumerate(context[line_number + 1:], start=line_number + 1):
                    if next_line.strip() == stripped_line:
                        is_terminated = True
                        break
                
                if not is_terminated:
                    findings.append(
                        Finding(
                            rule_id=self.id,
                            position=Position(line=line_number + 1),
                            message=f"Unterminated {self.block_markers[stripped_line]} starting",
                            severity=self.severity,
                            context=line
                        )
                    )
        
        return findings

class BlockSpacingRule(Rule):
    """Rule to check for proper spacing around blocks."""
    
    id = "BLOCK002"
    name = "Block Spacing Check"
    description = "Checks for proper blank lines around blocks"
    severity = Severity.WARNING

    def __init__(self):
        super().__init__()
        self.block_markers = {
            "----", "====", "****", "....", "____", "|===",
            "////", "++++"
        }
        self.open_blocks: Dict[str, int] = {}

    def check_line(self, line: str, line_number: int, context: List[str]) -> List[Finding]:
        findings = []
        stripped_line = line.strip()
        
        if stripped_line in self.block_markers:
            if stripped_line in self.open_blocks:
                # This is a closing delimiter
                if line_number + 1 < len(context):
                    next_line = context[line_number + 1].strip()
                    if next_line and not next_line.startswith('='):
                        findings.append(
                            Finding(
                                rule_id=self.id,
                                position=Position(line=line_number + 2),
                                message="Block should be followed by a blank line",
                                severity=self.severity,
                                context=context[line_number + 1]
                            )
                        )
                del self.open_blocks[stripped_line]
            else:
                # This is an opening delimiter
                if line_number > 0:
                    prev_line = context[line_number - 1].strip()
                    if prev_line and not prev_line.startswith('='):
                        findings.append(
                            Finding(
                                rule_id=self.id,
                                position=Position(line=line_number + 1),
                                message="Block should be preceded by a blank line",
                                severity=self.severity,
                                context=line
                            )
                        )
                self.open_blocks[stripped_line] = line_number
        
        return findings