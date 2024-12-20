# test_rule_registry.py - Tests for the rule registry
"""Tests for the rule registry functionality"""

import pytest
from asciidoc_linter.rules.base import Rule, RuleRegistry, Severity

class TestRuleOne(Rule):
    """First test rule"""
    id = "TestRuleOne"
    name = "Test Rule One"
    description = "First test rule"
    severity = Severity.WARNING

class TestRuleTwo(Rule):
    """Second test rule"""
    id = "TestRuleTwo"
    name = "Test Rule Two"
    description = "Second test rule"
    severity = Severity.ERROR

def test_rule_registry():
    """Test the rule registry functionality"""
    # Clear registry
    RuleRegistry._rules.clear()
    
    # Test registration
    RuleRegistry.register_rule(TestRuleOne)
    RuleRegistry.register_rule(TestRuleTwo)
    
    # Test getting a specific rule
    rule_class = RuleRegistry.get_rule("TestRuleOne")
    assert rule_class == TestRuleOne
    
    # Test getting all rules
    all_rules = RuleRegistry.get_all_rules()
    assert len(all_rules) == 2
    assert TestRuleOne in all_rules
    assert TestRuleTwo in all_rules
    
    # Test creating all rules
    rule_instances = RuleRegistry.create_all_rules()
    assert len(rule_instances) == 2
    assert isinstance(rule_instances[0], Rule)
    assert isinstance(rule_instances[1], Rule)
    
    # Test getting non-existent rule
    with pytest.raises(KeyError):
        RuleRegistry.get_rule("NonExistentRule")