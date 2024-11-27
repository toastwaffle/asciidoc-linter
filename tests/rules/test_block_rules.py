# test_block_rules.py - Tests for block rules

import unittest
from asciidoc_linter.rules.block_rules import UnterminatedBlockRule, BlockSpacingRule

class TestUnterminatedBlockRule(unittest.TestCase):
    def setUp(self):
        self.rule = UnterminatedBlockRule()

    def test_terminated_block(self):
        content = [
            "Some text",
            "----",
            "This is a listing block",
            "with multiple lines",
            "----",
            "More text"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 0)

    def test_unterminated_block(self):
        content = [
            "Some text",
            "----",
            "This is an unterminated block",
            "with no end marker",
            "More text"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line_number, 2)

    def test_multiple_blocks(self):
        content = [
            "====",
            "Example block",
            "====",
            "",
            "----",
            "Unterminated listing block",
            "",
            "****",
            "Sidebar content",
            "****"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)

class TestBlockSpacingRule(unittest.TestCase):
    def setUp(self):
        self.rule = BlockSpacingRule()

    def test_correct_spacing(self):
        content = [
            "Some text",
            "",
            "----",
            "Block content",
            "----",
            "",
            "More text"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 0)

    def test_missing_space_before(self):
        content = [
            "Some text",
            "----",
            "Block content",
            "----",
            "",
            "More text"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)
        self.assertTrue("preceded by" in findings[0].message)

    def test_missing_space_after(self):
        content = [
            "Some text",
            "",
            "----",
            "Block content",
            "----",
            "More text"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)
        self.assertTrue("followed by" in findings[0].message)

    def test_heading_exception(self):
        content = [
            "= Heading",
            "----",
            "Block content",
            "----",
            "= Another Heading"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 0)

if __name__ == '__main__':
    unittest.main()