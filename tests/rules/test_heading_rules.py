# test_heading_rules.py - Tests for heading rules
"""
Tests for all heading-related rules including:
- HeadingIncrementationRule (HEAD001)
- HeadingFormatRule (HEAD002)
- HeadingMultipleTopLevelRule (HEAD003)
"""

import unittest
from asciidoc_linter.rules import Finding, Severity, Position
from asciidoc_linter.heading_rules import HeadingIncrementationRule, HeadingFormatRule, MultipleTopLevelHeadingsRule

class TestHeadingFormatRule(unittest.TestCase):
    """Tests for HEAD002: Heading Format Rule"""
    
    def setUp(self):
        self.rule = HeadingFormatRule()
    
    def test_valid_format(self):
        """Test that valid heading formats produce no findings"""
        content = """
= Level 1
== Level 2
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 0)
    
    def test_invalid_format(self):
        """Test detection of invalid heading formats"""
        content = """=level 1
==level 2"""
        findings = self.rule.check(content)
        
        # Debug output
        print("\nExpected findings:")
        print("1. No space after = in line 1")
        print("2. Lowercase in line 1 ('level')")
        print("3. No space after == in line 2")
        print("4. Lowercase in line 2 ('level')")
        
        print("\nActual findings:")
        for i, f in enumerate(findings, 1):
            print(f"{i}. {f.message} (line {f.position.line}): {f.context}")
        
        # We expect 4 findings:
        # 1. No space after = in line 1
        # 2. Lowercase in line 1 ('level')
        # 3. No space after == in line 2
        # 4. Lowercase in line 2 ('level')
        self.assertEqual(len(findings), 4)
        self.assertTrue(all(f.rule_id == "HEAD002" for f in findings))
        
        # Verify specific findings
        space_findings = [f for f in findings if "Missing space" in f.message]
        case_findings = [f for f in findings if "uppercase" in f.message]
        
        self.assertEqual(len(space_findings), 2, "Should have two 'missing space' findings")
        self.assertEqual(len(case_findings), 2, "Should have two 'uppercase' findings")

class TestHeadingIncrementationRule(unittest.TestCase):
    """Tests for HEAD001: Heading Incrementation Rule"""
    
    def setUp(self):
        self.rule = HeadingIncrementationRule()
    
    def test_valid_heading_sequence(self):
        """Test that valid heading sequences produce no findings"""
        content = """
= Level 1
Some content

== Level 2
More content

=== Level 3
Even more content
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 0, "Valid heading sequence should not produce findings")
    
    def test_skipped_heading_level(self):
        """Test that skipped heading levels are detected"""
        content = """
= Level 1
Some content

=== Level 3
Skipped level 2!
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 1, "Skipped heading level should produce one finding")
        self.assertEqual(findings[0].severity, Severity.ERROR)
        self.assertTrue("skipped" in findings[0].message.lower())
    
    def test_multiple_skipped_levels(self):
        """Test that multiple skipped levels are detected"""
        content = """
= Level 1
Some content

==== Level 4
Skipped two levels!
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 1, "Skipped heading levels should produce one finding")
        self.assertEqual(findings[0].severity, Severity.ERROR)
    
    def test_empty_document(self):
        """Test handling of empty documents"""
        content = ""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 0, "Empty document should not produce findings")
    
    def test_no_headings(self):
        """Test handling of documents without headings"""
        content = """
This is a document
with no headings
just regular text
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 0, "Document without headings should not produce findings")
    
    def test_heading_underline_not_counted(self):
        """Test that heading underlines are not counted as headings"""
        content = """
Level 1
=======
Some content

Level 2
-------
More content
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 0, "Heading underlines should not be counted as headings")

class TestMultipleTopLevelHeadingsRule(unittest.TestCase):
    """Tests for HEAD003: Multiple Top-Level Headings Rule"""
    
    def setUp(self):
        self.rule = MultipleTopLevelHeadingsRule()
    
    def test_single_top_level(self):
        """Test that single top-level heading produces no findings"""
        content = """
= Document Title
== Section 1
== Section 2
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 0)
    
    def test_multiple_top_level(self):
        """Test detection of multiple top-level headings"""
        content = """
= First Title
== Section 1
= Second Title
== Section 2
"""
        findings = self.rule.check(content)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, Severity.ERROR)

if __name__ == '__main__':
    unittest.main()