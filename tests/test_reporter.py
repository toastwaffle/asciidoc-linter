# test_reporter.py - Tests for the reporter module
"""
Tests for the reporter module that handles formatting of lint results
"""

import json
import pytest
from asciidoc_linter.reporter import (
    LintError,
    LintReport,
    Reporter,
    JsonReporter,
    HtmlReporter
)

# Test Data

@pytest.fixture
def sample_error():
    """Create a sample lint error"""
    return LintError(
        file="test.adoc",
        line=42,
        message="Test error message"
    )

@pytest.fixture
def sample_report(sample_error):
    """Create a sample report with one error"""
    return LintReport([sample_error])

@pytest.fixture
def complex_report():
    """Create a more complex report with multiple errors"""
    return LintReport([
        LintError("doc1.adoc", 1, "First error"),
        LintError("doc1.adoc", 5, "Second error"),
        LintError("doc2.adoc", 10, "Error in another file"),
        LintError(None, 15, "Error without file")
    ])

# Test LintError

def test_lint_error_creation():
    """Test creating a LintError"""
    error = LintError("test.adoc", 42, "Test message")
    assert error.file == "test.adoc"
    assert error.line == 42
    assert error.message == "Test message"

# Test LintReport

def test_lint_report_creation(sample_error):
    """Test creating a LintReport"""
    report = LintReport([sample_error])
    assert len(report.errors) == 1
    assert report.errors[0] == sample_error

def test_lint_report_bool(sample_report):
    """Test boolean evaluation of LintReport"""
    assert bool(sample_report) is True
    assert bool(LintReport([])) is False

def test_lint_report_len(complex_report):
    """Test len() on LintReport"""
    assert len(complex_report) == 4

# Test Base Reporter

def test_base_reporter_format(sample_report):
    """Test the base reporter's format_report method"""
    reporter = Reporter()
    output = reporter.format_report(sample_report)
    assert "test.adoc:line 42: Test error message" in output

def test_base_reporter_multiple_errors(complex_report):
    """Test formatting multiple errors"""
    reporter = Reporter()
    output = reporter.format_report(complex_report)
    assert "doc1.adoc:line 1: First error" in output
    assert "doc1.adoc:line 5: Second error" in output
    assert "doc2.adoc:line 10: Error in another file" in output
    assert "line 15: Error without file" in output

# Test JSON Reporter

def test_json_reporter_format(sample_report):
    """Test JSON formatting of a report"""
    reporter = JsonReporter()
    output = reporter.format_report(sample_report)
    data = json.loads(output)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["file"] == "test.adoc"
    assert data[0]["line"] == 42
    assert data[0]["message"] == "Test error message"

def test_json_reporter_complex(complex_report):
    """Test JSON formatting of a complex report"""
    reporter = JsonReporter()
    output = reporter.format_report(complex_report)
    data = json.loads(output)
    assert len(data) == 4
    assert data[0]["file"] == "doc1.adoc"
    assert data[3]["file"] is None

# Test HTML Reporter

def test_html_reporter_format(sample_report):
    """Test HTML formatting of a report"""
    reporter = HtmlReporter()
    output = reporter.format_report(sample_report)
    assert "<!DOCTYPE html>" in output
    assert "<table>" in output
    assert "test.adoc:Line 42" in output
    assert "Test error message" in output

def test_html_reporter_complex(complex_report):
    """Test HTML formatting of a complex report"""
    reporter = HtmlReporter()
    output = reporter.format_report(complex_report)
    assert "doc1.adoc:Line 1" in output
    assert "First error" in output
    assert "doc2.adoc:Line 10" in output
    assert "Error without file" in output

def test_html_reporter_styling(sample_report):
    """Test that HTML output includes CSS styling"""
    reporter = HtmlReporter()
    output = reporter.format_report(sample_report)
    assert "<style>" in output
    assert "table {" in output
    assert "border-collapse: collapse" in output