#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=expense_doc --cov-report=html --cov-report=term-missing tests/

# Run linting
flake8 expense_doc
mypy expense_doc

# Deactivate virtual environment
deactivate 