# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=expense_doc --cov-report=html --cov-report=term-missing tests/

# Run linting
flake8 expense_doc
mypy expense_doc

# Deactivate virtual environment
deactivate 