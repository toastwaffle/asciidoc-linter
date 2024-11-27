# test_whitespace_rules.py - Tests for whitespace rules

import unittest
from asciidoc_linter.rules.whitespace_rules import WhitespaceRule

class TestWhitespaceRule(unittest.TestCase):
    def setUp(self):
        self.rule = WhitespaceRule()

    def test_multiple_empty_lines(self):
        content = [
            "First line",
            "",
            "",
            "",
            "Last line"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)
        self.assertTrue("consecutive empty line" in findings[0].message)

    def test_list_marker_spacing(self):
        content = [
            "* Valid item",
            "*Invalid item",
            "- Valid item",
            "-Invalid item",
            ". Valid item",
            ".Invalid item"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 3)
        for finding in findings:
            self.assertTrue("space after the marker" in finding.message)

    def test_admonition_block_spacing(self):
        content = [
            "Some text",
            "NOTE: This needs a blank line",
            "",
            "IMPORTANT: This is correct",
            "More text",
            "WARNING: This needs a blank line"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 2)
        for finding in findings:
            self.assertTrue("preceded by a blank line" in finding.message)

    def test_trailing_whitespace(self):
        content = [
            "Line without trailing space",
            "Line with trailing space ",
            "Another clean line",
            "More trailing space  "
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 2)
        for finding in findings:
            self.assertTrue("trailing whitespace" in finding.message)

    def test_tabs(self):
        content = [
            "Normal line",
            "\tLine with tab",
            "    Spaces are fine",
            "\tAnother tab"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 2)
        for finding in findings:
            self.assertTrue("contains tabs" in finding.message)

    def test_section_title_spacing(self):
        content = [
            "Some text",
            "== Section Title",
            "No space after",
            "",
            "=== Another Section",
            "",
            "This is correct"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 2)
        self.assertTrue(any("preceded by" in f.message for f in findings))
        self.assertTrue(any("followed by" in f.message for f in findings))

    def test_valid_document(self):
        content = [
            "= Document Title",
            "",
            "== Section 1",
            "",
            "* List item 1",
            "* List item 2",
            "",
            "NOTE: Important note",
            "",
            "=== Subsection",
            "",
            "Normal paragraph."
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 0)