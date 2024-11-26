# reporter.py - Output formatters for lint results
"""
Different output formatters for lint results
"""

import json
from abc import ABC, abstractmethod
from typing import List
from .rules import Finding

class Reporter(ABC):
    """Base class for all reporters"""
    
    @abstractmethod
    def report(self, findings: List[Finding]) -> str:
        """Format and return the findings"""
        pass

class ConsoleReporter(Reporter):
    """Reports findings to the console in a human-readable format"""
    
    def report(self, findings: List[Finding]) -> str:
        output = []
        for finding in findings:
            severity = finding.severity.value.upper()
            location = f"line {finding.position.line}"
            if finding.position.column:
                location += f", column {finding.position.column}"
            
            output.append(
                f"{severity}: {finding.message} ({finding.rule_id})"
                f"\n  at {location}"
            )
            if finding.context:
                output.append(f"  context: {finding.context}")
        
        return "\n".join(output)

class JsonReporter(Reporter):
    """Reports findings in JSON format"""
    
    def report(self, findings: List[Finding]) -> str:
        return json.dumps([
            {
                'rule_id': f.rule_id,
                'message': f.message,
                'severity': f.severity.value,
                'position': {
                    'line': f.position.line,
                    'column': f.position.column
                },
                'context': f.context
            }
            for f in findings
        ], indent=2)

class HtmlReporter(Reporter):
    """Reports findings in HTML format"""
    
    def report(self, findings: List[Finding]) -> str:
        rows = []
        for f in findings:
            severity_class = f"severity-{f.severity.value}"
            rows.append(
                f'<tr class="{severity_class}">'
                f'<td>{f.severity.value.upper()}</td>'
                f'<td>{f.rule_id}</td>'
                f'<td>{f.message}</td>'
                f'<td>Line {f.position.line}</td>'
                f'</tr>'
            )
        
        return f"""
        <html>
        <head>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .severity-error {{ background-color: #ffe6e6; }}
                .severity-warning {{ background-color: #fff3e6; }}
                .severity-info {{ background-color: #e6f3ff; }}
            </style>
        </head>
        <body>
            <h1>AsciiDoc Lint Results</h1>
            <table>
                <tr>
                    <th>Severity</th>
                    <th>Rule</th>
                    <th>Message</th>
                    <th>Location</th>
                </tr>
                {"".join(rows)}
            </table>
        </body>
        </html>
        """