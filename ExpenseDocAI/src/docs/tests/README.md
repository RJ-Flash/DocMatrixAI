# ExpenseDocAI Documentation Tests

This directory contains tests to validate the ExpenseDocAI API documentation and examples.

## Overview

The test suite ensures that:
1. All API endpoints documented in `api.rst` are functional
2. Code examples in the documentation are accurate and working
3. SDK integration examples are valid
4. Documentation links are not broken
5. API responses match documented schemas

## Setup

1. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # On Windows
   source .venv/bin/activate   # On Unix/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov requests
   ```

3. Configure environment variables:
   ```bash
   # Windows PowerShell
   $env:API_BASE_URL = "https://api.expensedocai.com/api/v1"
   $env:API_KEY = "your_api_key"
   $env:TEST_USERNAME = "test_user"
   $env:TEST_PASSWORD = "test_pass"

   # Unix/macOS
   export API_BASE_URL="https://api.expensedocai.com/api/v1"
   export API_KEY="your_api_key"
   export TEST_USERNAME="test_user"
   export TEST_PASSWORD="test_pass"
   ```

## Running Tests

### Using the Validation Script

Run the complete validation suite:
```powershell
.\validate_api.ps1
```

This will:
1. Set up the environment
2. Run API tests
3. Build documentation
4. Check links
5. Run doctests
6. Open coverage report and documentation

### Manual Test Execution

Run specific test categories:

```bash
# Run all tests
pytest tests/test_api_examples.py -v

# Run with coverage
pytest tests/test_api_examples.py -v --cov=tests --cov-report=html

# Run specific test categories
pytest tests/test_api_examples.py -v -m api
pytest tests/test_api_examples.py -v -m docs
pytest tests/test_api_examples.py -v -m integration
```

## Test Categories

- `@pytest.mark.api`: Tests that validate API endpoints
- `@pytest.mark.docs`: Tests for documentation examples
- `@pytest.mark.integration`: Integration tests with external services
- `@pytest.mark.unit`: Unit tests for utilities

## Test Data

The `test_data` directory contains:
- `sample_receipt.pdf`: Sample receipt for document upload tests
- Other test files as needed

## Coverage Reports

After running tests with coverage:
1. HTML report: `coverage_html/index.html`
2. XML report: `coverage.xml` (used by CI/CD)

## Continuous Integration

Tests are automatically run on GitHub Actions:
1. On every push to `main` branch
2. On pull requests affecting documentation
3. Results are uploaded to Codecov

## Troubleshooting

Common issues and solutions:

1. **API Connection Issues**:
   - Verify environment variables
   - Check API key permissions
   - Ensure network connectivity

2. **Test Failures**:
   - Check test data is present
   - Verify API responses match documentation
   - Review error messages in test output

3. **Documentation Build Issues**:
   - Ensure Sphinx is installed
   - Check RST syntax
   - Verify all referenced files exist

## Contributing

When adding new tests:
1. Follow existing test patterns
2. Add appropriate markers
3. Update this README if needed
4. Include test data if required
5. Verify coverage is maintained

## Support

For test-related issues:
1. Check the troubleshooting section
2. Review GitHub Actions logs
3. Contact the development team 