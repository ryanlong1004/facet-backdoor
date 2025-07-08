#!/bin/bash
# Run lint, tests, code formatting, and import sorting for the project

set -e

# Lint
echo "Running flake8..."
flake8 .

# Tests
echo "Running pytest..."
pytest

# Beautify (black)
echo "Running black..."
black .

# isort
echo "Running isort..."
isort .

echo "All checks and formatting complete."
