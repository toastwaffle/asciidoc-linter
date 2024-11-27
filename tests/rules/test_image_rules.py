# test_image_rules.py - Tests for image rules

import unittest
from pathlib import Path
from asciidoc_linter.rules.image_rules import ImageAttributesRule

class TestImageAttributesRule(unittest.TestCase):
    def setUp(self):
        self.rule = ImageAttributesRule()
        
    def test_inline_image_without_alt(self):
        content = [
            "Here is an image:test.png[] without alt text."
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 2)  # Missing alt text and file not found
        self.assertTrue(any("Missing alt text" in f.message for f in findings))
        
    def test_inline_image_with_alt(self):
        content = [
            "Here is an image:test.png[A good description of the image] with alt text."
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)  # Only file not found
        
    def test_block_image_complete(self):
        content = [
            "image::test.png[Alt text for image, title=Image Title, width=500]"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)  # Only file not found
        
    def test_block_image_missing_attributes(self):
        content = [
            "image::test.png[]"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 3)  # Missing alt, title, size + file not found
        
    def test_short_alt_text(self):
        content = [
            "image:test.png[img]"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertTrue(any("Alt text too short" in f.message for f in findings))
        
    def test_external_url(self):
        content = [
            "image:https://example.com/test.png[External image]"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 0)  # External URLs are not checked for existence
        
    def test_multiple_images_per_line(self):
        content = [
            "Here are two images: image:test1.png[] and image:test2.png[Good alt text]"
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 3)  # First image: missing alt + not found, Second image: not found
        
    def test_attribute_parsing(self):
        content = [
            'image::test.png[Alt text, title="Complex, title with, commas", width=500]'
        ]
        findings = []
        for i, line in enumerate(content):
            findings.extend(self.rule.check_line(line, i, content))
        self.assertEqual(len(findings), 1)  # Only file not found
        
    def test_valid_local_image(self):
        # Create a temporary test image
        test_image = Path("test_image.png")
        test_image.touch()
        
        try:
            content = [
                'image::test_image.png[Valid test image, title="Test Image", width=500]'
            ]
            findings = []
            for i, line in enumerate(content):
                findings.extend(self.rule.check_line(line, i, content))
            self.assertEqual(len(findings), 0)  # All valid
        finally:
            # Clean up
            test_image.unlink()

if __name__ == '__main__':
    unittest.main()