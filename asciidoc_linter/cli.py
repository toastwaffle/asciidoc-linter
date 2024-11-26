# cli.py - Command line interface
"""
Command line interface for the AsciiDoc linter
"""

import argparse
import sys
from typing import List, Optional
from pathlib import Path
from .linter import AsciiDocLinter
from .reporter import ConsoleReporter, JsonReporter, HtmlReporter

def create_parser() -> argparse.ArgumentParser:
    """Create the command line parser"""
    parser = argparse.ArgumentParser(
        description='Lint AsciiDoc files for common issues and style violations'
    )
    parser.add_argument(
        'files',
        nargs='+',
        help='One or more AsciiDoc files to check'
    )
    parser.add_argument(
        '--config',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--format',
        choices=['console', 'json', 'html'],
        default='console',
        help='Output format (default: console)'
    )
    return parser

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the linter"""
    if args is None:
        args = sys.argv[1:]
    
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Create linter instance
    linter = AsciiDocLinter()
    
    # Set reporter based on format argument
    if parsed_args.format == 'json':
        linter.set_reporter(JsonReporter())
    elif parsed_args.format == 'html':
        linter.set_reporter(HtmlReporter())
    
    exit_code = 0
    
    # Process each file
    for file_path in parsed_args.files:
        path = Path(file_path)
        if not path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            exit_code = 1
            continue
        
        try:
            content = path.read_text()
            results = linter.lint(content)
            
            # Print results
            if results:
                print(f"\nResults for {file_path}:")
                print(results)
                exit_code = 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
            exit_code = 1
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())