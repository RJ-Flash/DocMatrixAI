# Test Data for ExpenseDocAI Documentation Tests

This directory contains test data files used by the ExpenseDocAI documentation tests.

## Files

### `sample_receipt.pdf`
A sample receipt file used for testing document upload and processing functionality.

**Content:**
- Receipt Number: TEST-001
- Date: 2024-02-20
- Vendor: Office Supplies Inc.
- Items:
  - Printer Paper (2 x $25.00 = $50.00)
  - Ink Cartridges (3 x $20.00 = $60.00)
- Subtotal: $110.00
- Tax (10%): $11.00
- Total: $121.00

**Usage:**
- Used in `test_document_upload()` to test file upload functionality
- Used in `test_document_detail()` to test document processing
- Used in `test_sdk_integration()` to test SDK functionality

## Adding New Test Files

When adding new test files:

1. Keep files small and focused
2. Document the file's purpose and content
3. Update this README
4. Ensure files are committed to version control
5. Add appropriate test cases

## File Requirements

- PDF files should be valid and readable
- Images should be clear and properly formatted
- Text should be machine-readable
- Files should be under 1MB in size
- Include realistic but non-sensitive data

## Maintenance

Test files should be reviewed periodically to ensure:
1. They remain valid and useful
2. They match current API requirements
3. They cover necessary test cases
4. They don't contain outdated information

## Support

For issues with test files:
1. Check file format and content
2. Verify file permissions
3. Contact development team if needed 