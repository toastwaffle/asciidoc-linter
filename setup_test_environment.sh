#!/bin/bash
# setup_test_environment.sh - Setup script for test environment

echo "Setting up test environment..."

# Upgrade pip
python -m pip install --upgrade pip

# Install test dependencies
pip install pytest pytest-cov pytest-html pytest-metadata

# Install project with test dependencies
pip install -e ".[test]"

echo "Test environment setup complete. You can now run: python run_tests_html.py"