# test_linter.py - Tests for the main linter module
"""
Tests for the main linter module (linter.py)
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from asciidoc_linter.linter import AsciiDocLinter
from asciidoc_linter.parser import AsciiDocParser
from asciidoc_linter.reporter import LintReport, LintError

# Fixtures

@pytest.fixture
def mock_parser():
    """Create a mock parser that returns a simple document structure"""
    parser = Mock(spec=AsciiDocParser)
    parser.parse.return_value = {
        'type': 'document',
        'content': []
    }
    return parser

@pytest.fixture
def mock_rule():
    """Create a mock rule that can be configured to return specific errors"""
    rule = Mock()
    rule.check.return_value = []  # By default, return no errors
    return rule

@pytest.fixture
def sample_asciidoc():
    """Return a sample AsciiDoc string for testing"""
    return """= Title

== Section 1

Some content.

== Section 2

More content.
"""

# Tests for initialization

def test_linter_initialization():
    """Test that the linter initializes with correct default rules"""
    linter = AsciiDocLinter()
    assert len(linter.rules) == 7  # Verify number of default rules
    assert hasattr(linter, 'parser')  # Verify parser is initialized

# Tests for lint_string method

def test_lint_string_no_errors(mock_parser, mock_rule):
    """Test linting a string with no errors"""
    with patch('asciidoc_linter.linter.AsciiDocParser', return_value=mock_parser):
        linter = AsciiDocLinter()
        linter.rules = [mock_rule]
        
        report = linter.lint_string("Some content")
        
        assert isinstance(report, LintReport)
        assert len(report.errors) == 0
        mock_parser.parse.assert_called_once_with("Some content")
        mock_rule.check.assert_called_once()

def test_lint_string_with_errors(mock_parser, mock_rule):
    """Test linting a string that contains errors"""
    mock_rule.check.return_value = [
        LintError(file=None, line=1, message="Test error")
    ]
    
    with patch('asciidoc_linter.linter.AsciiDocParser', return_value=mock_parser):
        linter = AsciiDocLinter()
        linter.rules = [mock_rule]
        
        report = linter.lint_string("Some content", source="test.adoc")
        
        assert len(report.errors) == 1
        assert report.errors[0].file == "test.adoc"
        assert report.errors[0].line == 1
        assert report.errors[0].message == "Test error"

def test_lint_string_multiple_rules(mock_parser):
    """Test that all rules are applied when linting a string"""
    rule1 = Mock()
    rule1.check.return_value = [LintError(file=None, line=1, message="Error 1")]
    rule2 = Mock()
    rule2.check.return_value = [LintError(file=None, line=2, message="Error 2")]
    
    with patch('asciidoc_linter.linter.AsciiDocParser', return_value=mock_parser):
        linter = AsciiDocLinter()
        linter.rules = [rule1, rule2]
        
        report = linter.lint_string("Some content")
        
        assert len(report.errors) == 2
        assert rule1.check.called
        assert rule2.check.called

# Tests for lint_file method

def test_lint_file_success(tmp_path, sample_asciidoc):
    """Test linting a file that exists and is readable"""
    test_file = tmp_path / "test.adoc"
    test_file.write_text(sample_asciidoc)
    
    linter = AsciiDocLinter()
    report = linter.lint_file(test_file)
    
    assert isinstance(report, LintReport)
    # Note: actual number of errors depends on the rules

def test_lint_file_not_found():
    """Test linting a file that doesn't exist"""
    non_existent_file = Path("non_existent.adoc")
    
    linter = AsciiDocLinter()
    report = linter.lint_file(non_existent_file)
    
    assert len(report.errors) == 1
    assert "Error reading file" in report.errors[0].message

def test_lint_file_with_source_tracking(tmp_path, sample_asciidoc, mock_rule):
    """Test that file source is correctly tracked in errors"""
    test_file = tmp_path / "test.adoc"
    test_file.write_text(sample_asciidoc)
    
    mock_rule.check.return_value = [
        LintError(file=None, line=1, message="Test error")
    ]
    
    linter = AsciiDocLinter()
    linter.rules = [mock_rule]
    
    report = linter.lint_file(test_file)
    
    assert len(report.errors) == 1
    assert str(test_file) == report.errors[0].file

# Integration tests

def test_integration_with_real_rules():
    """Test the linter with actual rules and a sample document"""
    linter = AsciiDocLinter()
    sample_doc = """= Title
    
== Section 1

Some content.

=== Subsection

More content.
"""
    
    report = linter.lint_string(sample_doc)
    assert isinstance(report, LintReport)
    # Note: actual number of errors depends on the implemented rules