# test_rules.py - Tests for rules module
"""Tests for the rules module and base functionality"""

import unittest
from asciidoc_linter.rules import (
    Severity,
    Position,
    Finding,
    Rule,
    RuleRegistry
)

class TestSeverity(unittest.TestCase):
    """Test the Severity enum"""
    
    def test_severity_values(self):
        """Test that Severity enum has correct values"""
        self.assertEqual(Severity.INFO.value, "info")
        self.assertEqual(Severity.WARNING.value, "warning")
        self.assertEqual(Severity.ERROR.value, "error")
    
    def test_severity_comparison(self):
        """Test that Severity values can be compared"""
        self.assertNotEqual(Severity.INFO, Severity.ERROR)
        self.assertEqual(Severity.WARNING, Severity.WARNING)

class TestPosition(unittest.TestCase):
    """Test the Position class"""
    
    def test_position_with_line_and_column(self):
        """Test Position with both line and column"""
        pos = Position(10, 5)
        self.assertEqual(pos.line, 10)
        self.assertEqual(pos.column, 5)
        self.assertEqual(str(pos), "line 10, column 5")
    
    def test_position_with_line_only(self):
        """Test Position with line only"""
        pos = Position(10)
        self.assertEqual(pos.line, 10)
        self.assertIsNone(pos.column)
        self.assertEqual(str(pos), "line 10")

class TestFinding(unittest.TestCase):
    """Test the Finding class"""
    
    def setUp(self):
        """Set up test data"""
        self.position = Position(10, 5)
        self.finding = Finding(
            rule_id="TEST001",
            position=self.position,
            message="Test message",
            severity=Severity.WARNING,
            context="Test context"
        )
    
    def test_finding_creation(self):
        """Test Finding creation with all attributes"""
        self.assertEqual(self.finding.rule_id, "TEST001")
        self.assertEqual(self.finding.position, self.position)
        self.assertEqual(self.finding.message, "Test message")
        self.assertEqual(self.finding.severity, Severity.WARNING)
        self.assertEqual(self.finding.context, "Test context")
    
    def test_line_number_property(self):
        """Test line_number property"""
        self.assertEqual(self.finding.line_number, 10)

class TestRule(unittest.TestCase):
    """Test the Rule base class"""
    
    class TestRule(Rule):
        """Test implementation of Rule"""
        id = "TEST001"
        name = "Test Rule"
        description = "Rule for testing"
        severity = Severity.WARNING
        
        def check_line_content(self, line: str, line_number: int):
            """Test implementation that finds 'ERROR' in lines"""
            if "ERROR" in line:
                return [self.create_finding(line_number, "Found ERROR")]
            return []
        
        def check_line_context(self, line, line_number, prev_line, next_line):
            """Test implementation that checks for repeated lines"""
            if prev_line and line == prev_line:
                return [self.create_finding(line_number, "Repeated line")]
            return []
    
    def setUp(self):
        """Set up test data"""
        self.rule = self.TestRule()
    
    def test_rule_attributes(self):
        """Test basic rule attributes"""
        self.assertEqual(self.rule.id, "TEST001")
        self.assertEqual(self.rule.name, "Test Rule")
        self.assertEqual(self.rule.description, "Rule for testing")
        self.assertEqual(self.rule.severity, Severity.WARNING)
    
    def test_check_line(self):
        """Test check_line with various scenarios"""
        # Test single line with error
        findings = self.rule.check_line("This has an ERROR", 0, ["This has an ERROR"])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].message, "Found ERROR")
        
        # Test repeated lines
        context = ["Same line", "Same line"]
        findings = self.rule.check_line("Same line", 1, context)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].message, "Repeated line")
    
    def test_create_finding(self):
        """Test create_finding helper method"""
        finding = self.rule.create_finding(10, "Test message", 5, "Test context")
        self.assertEqual(finding.rule_id, "TEST001")
        self.assertEqual(finding.position.line, 10)
        self.assertEqual(finding.position.column, 5)
        self.assertEqual(finding.message, "Test message")
        self.assertEqual(finding.severity, Severity.WARNING)
        self.assertEqual(finding.context, "Test context")

class TestRuleRegistry(unittest.TestCase):
    """Test the RuleRegistry"""
    
    class TestRule1(Rule):
        """First test rule"""
        id = "TEST001"
    
    class TestRule2(Rule):
        """Second test rule"""
        id = "TEST002"
    
    def setUp(self):
        """Set up test data"""
        # Clear registry before each test
        RuleRegistry._rules = {}
    
    def test_register_rule(self):
        """Test rule registration"""
        RuleRegistry.register_rule(self.TestRule1)
        self.assertIn(self.TestRule1.__name__, RuleRegistry._rules)
        self.assertEqual(RuleRegistry._rules[self.TestRule1.__name__], self.TestRule1)
    
    def test_get_rule(self):
        """Test getting a rule by name"""
        RuleRegistry.register_rule(self.TestRule1)
        rule_class = RuleRegistry.get_rule(self.TestRule1.__name__)
        self.assertEqual(rule_class, self.TestRule1)
    
    def test_get_all_rules(self):
        """Test getting all registered rules"""
        RuleRegistry.register_rule(self.TestRule1)
        RuleRegistry.register_rule(self.TestRule2)
        rules = RuleRegistry.get_all_rules()
        self.assertEqual(len(rules), 2)
        self.assertIn(self.TestRule1, rules)
        self.assertIn(self.TestRule2, rules)
    
    def test_create_all_rules(self):
        """Test creating instances of all rules"""
        RuleRegistry.register_rule(self.TestRule1)
        RuleRegistry.register_rule(self.TestRule2)
        instances = RuleRegistry.create_all_rules()
        self.assertEqual(len(instances), 2)
        self.assertTrue(any(isinstance(rule, self.TestRule1) for rule in instances))
        self.assertTrue(any(isinstance(rule, self.TestRule2) for rule in instances))
    
    def test_get_nonexistent_rule(self):
        """Test getting a rule that doesn't exist"""
        with self.assertRaises(KeyError):
            RuleRegistry.get_rule("NonexistentRule")

if __name__ == '__main__':
    unittest.main()