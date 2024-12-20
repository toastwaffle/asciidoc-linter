# test_cli.py - Tests for command line interface
"""Tests for the command line interface"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from asciidoc_linter.cli import main, create_parser
from asciidoc_linter.reporter import ConsoleReporter, JsonReporter, HtmlReporter

class TestCliArgumentParsing(unittest.TestCase):
    """Test argument parsing functionality"""
    
    def test_create_parser(self):
        """Test parser creation and default values"""
        parser = create_parser()
        args = parser.parse_args(['test.adoc'])
        
        self.assertEqual(args.files, ['test.adoc'])
        self.assertEqual(args.format, 'console')
        self.assertIsNone(args.config)
    
    def test_multiple_files(self):
        """Test parsing multiple file arguments"""
        parser = create_parser()
        args = parser.parse_args(['file1.adoc', 'file2.adoc'])
        
        self.assertEqual(args.files, ['file1.adoc', 'file2.adoc'])
    
    def test_format_option(self):
        """Test different format options"""
        parser = create_parser()
        
        # Test console format
        args = parser.parse_args(['test.adoc', '--format', 'console'])
        self.assertEqual(args.format, 'console')
        
        # Test JSON format
        args = parser.parse_args(['test.adoc', '--format', 'json'])
        self.assertEqual(args.format, 'json')
        
        # Test HTML format
        args = parser.parse_args(['test.adoc', '--format', 'html'])
        self.assertEqual(args.format, 'html')
    
    def test_config_option(self):
        """Test config file option"""
        parser = create_parser()
        args = parser.parse_args(['test.adoc', '--config', 'config.yml'])
        
        self.assertEqual(args.config, 'config.yml')
    
    def test_invalid_format(self):
        """Test invalid format option"""
        parser = create_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(['test.adoc', '--format', 'invalid'])

class TestCliFileProcessing(unittest.TestCase):
    """Test file processing functionality"""
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_file_not_found(self, mock_read_text, mock_exists):
        """Test handling of non-existent files"""
        mock_exists.return_value = False
        
        with patch('sys.stderr') as mock_stderr:
            exit_code = main(['nonexistent.adoc'])
        
        self.assertEqual(exit_code, 1)
        mock_read_text.assert_not_called()
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_file_read_error(self, mock_read_text, mock_exists):
        """Test handling of unreadable files"""
        mock_exists.return_value = True
        mock_read_text.side_effect = PermissionError("Permission denied")
        
        with patch('sys.stderr') as mock_stderr:
            exit_code = main(['unreadable.adoc'])
        
        self.assertEqual(exit_code, 1)
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    @patch('asciidoc_linter.linter.AsciiDocLinter.lint')
    def test_successful_lint(self, mock_lint, mock_read_text, mock_exists):
        """Test successful file linting"""
        mock_exists.return_value = True
        mock_read_text.return_value = "= Test Document"
        mock_lint.return_value = []  # No lint errors
        
        exit_code = main(['valid.adoc'])
        
        self.assertEqual(exit_code, 0)
        mock_lint.assert_called_once()
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    @patch('asciidoc_linter.linter.AsciiDocLinter.lint')
    def test_lint_with_errors(self, mock_lint, mock_read_text, mock_exists):
        """Test file linting with errors"""
        mock_exists.return_value = True
        mock_read_text.return_value = "= Test Document"
        mock_lint.return_value = ["Error: Invalid heading"]  # Simulate lint error
        
        exit_code = main(['invalid.adoc'])
        
        self.assertEqual(exit_code, 1)
        mock_lint.assert_called_once()

class TestCliReporters(unittest.TestCase):
    """Test reporter selection and usage"""
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    @patch('asciidoc_linter.linter.AsciiDocLinter.set_reporter')
    def test_json_reporter(self, mock_set_reporter, mock_read_text, mock_exists):
        """Test JSON reporter selection"""
        mock_exists.return_value = True
        
        main(['test.adoc', '--format', 'json'])
        
        # Verify that JsonReporter was set
        mock_set_reporter.assert_called_once()
        reporter = mock_set_reporter.call_args[0][0]
        self.assertIsInstance(reporter, JsonReporter)
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    @patch('asciidoc_linter.linter.AsciiDocLinter.set_reporter')
    def test_html_reporter(self, mock_set_reporter, mock_read_text, mock_exists):
        """Test HTML reporter selection"""
        mock_exists.return_value = True
        
        main(['test.adoc', '--format', 'html'])
        
        # Verify that HtmlReporter was set
        mock_set_reporter.assert_called_once()
        reporter = mock_set_reporter.call_args[0][0]
        self.assertIsInstance(reporter, HtmlReporter)
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    @patch('asciidoc_linter.linter.AsciiDocLinter.set_reporter')
    def test_default_console_reporter(self, mock_set_reporter, mock_read_text, mock_exists):
        """Test default console reporter"""
        mock_exists.return_value = True
        
        main(['test.adoc'])  # No format specified
        
        # Verify that no reporter was set (uses default ConsoleReporter)
        mock_set_reporter.assert_not_called()

if __name__ == '__main__':
    unittest.main()