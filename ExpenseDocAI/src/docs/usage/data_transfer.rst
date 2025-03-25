Data Export and Import Guide
========================

This guide explains how to manage data exports and imports in ExpenseDocAI.

Export Types
----------

ExpenseDocAI supports various export types:

1. **Expense Exports**
   ~~~~~~~~~~~~~~~

   Configure expense data exports:

   .. code-block:: json

      {
          "expense_export": {
              "format": "csv",
              "filters": {
                  "date_range": {
                      "start": "2024-01-01",
                      "end": "2024-12-31"
                  },
                  "categories": ["travel", "meals"],
                  "status": ["approved", "reimbursed"],
                  "min_amount": 100.00
              },
              "fields": [
                  "expense_id",
                  "date",
                  "category",
                  "amount",
                  "currency",
                  "vendor",
                  "description",
                  "status"
              ],
              "options": {
                  "include_attachments": true,
                  "zip_files": true,
                  "max_file_size": "100MB"
              }
          }
      }

2. **Report Exports**
   ~~~~~~~~~~~~~~

   Configure report exports:

   .. code-block:: json

      {
          "report_export": {
              "format": "excel",
              "reports": [
                  {
                      "type": "expense_summary",
                      "period": "monthly",
                      "grouping": ["category", "department"]
                  },
                  {
                      "type": "policy_compliance",
                      "period": "quarterly",
                      "metrics": ["violation_count", "resolution_time"]
                  }
              ],
              "options": {
                  "include_charts": true,
                  "password_protect": true,
                  "sheet_names": {
                      "summary": "Expense Summary",
                      "compliance": "Policy Compliance"
                  }
              }
          }
      }

Export Configuration
-----------------

Configure exports through the API:

1. **Create Export**:

   .. code-block:: python

      def create_export(export_data, api_token):
          url = 'http://example.com/api/v1/exports/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=export_data
          )
          
          return response.json()

2. **Schedule Export**:

   .. code-block:: python

      def schedule_export(schedule_data, api_token):
          url = 'http://example.com/api/v1/exports/schedule/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'export_id': schedule_data['export_id'],
                  'frequency': schedule_data['frequency'],
                  'recipients': schedule_data['recipients'],
                  'delivery_method': schedule_data['delivery_method']
              }
          )
          
          return response.json()

Import Types
----------

Configure data imports:

1. **Expense Import**:

   .. code-block:: json

      {
          "expense_import": {
              "source": "csv",
              "mapping": {
                  "date": "expense_date",
                  "amount": "total_amount",
                  "category": "expense_type",
                  "vendor": "merchant_name",
                  "description": "expense_details"
              },
              "validation": {
                  "required_fields": [
                      "date",
                      "amount",
                      "category"
                  ],
                  "date_format": "YYYY-MM-DD",
                  "amount_format": "decimal"
              },
              "options": {
                  "skip_header": true,
                  "batch_size": 1000,
                  "duplicate_check": true
              }
          }
      }

2. **Bulk Import**:

   .. code-block:: python

      def bulk_import(import_data, api_token):
          url = 'http://example.com/api/v1/imports/bulk/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'file_url': import_data['file_url'],
                  'import_type': import_data['import_type'],
                  'mapping': import_data['mapping'],
                  'options': import_data['options']
              }
          )
          
          return response.json()

Data Validation
------------

Configure import validation:

1. **Validation Rules**:

   .. code-block:: json

      {
          "validation_rules": {
              "date": {
                  "type": "date",
                  "format": "YYYY-MM-DD",
                  "min": "2020-01-01",
                  "required": true
              },
              "amount": {
                  "type": "decimal",
                  "min": 0.01,
                  "max": 10000.00,
                  "required": true
              },
              "category": {
                  "type": "string",
                  "allowed": ["travel", "meals", "office"],
                  "required": true
              },
              "vendor": {
                  "type": "string",
                  "max_length": 100,
                  "required": false
              }
          }
      }

2. **Validation Process**:

   .. code-block:: python

      def validate_import(validation_data, api_token):
          url = 'http://example.com/api/v1/imports/validate/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=validation_data
          )
          
          return response.json()

Error Handling
------------

Configure error handling:

1. **Error Configuration**:

   .. code-block:: json

      {
          "error_handling": {
              "on_error": "continue",
              "error_threshold": 100,
              "log_errors": true,
              "notification": {
                  "email": "admin@example.com",
                  "threshold": 10
              },
              "retry": {
                  "attempts": 3,
                  "delay": 300
              }
          }
      }

2. **Error Processing**:

   .. code-block:: python

      def process_errors(error_data, api_token):
          url = 'http://example.com/api/v1/imports/errors/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=error_data
          )
          
          return response.json()

Best Practices
------------

1. **Export Design**:
   
   * Clear formats
   * Useful filters
   * Complete data
   * Secure delivery
   * Regular schedule

2. **Import Design**:
   
   * Clean data
   * Clear mapping
   * Strict validation
   * Error handling
   * Audit trail

3. **Performance**:
   
   * Batch processing
   * Efficient formats
   * Data compression
   * Progress tracking
   * Resource monitoring

Troubleshooting
-------------

Common data transfer issues and solutions:

1. **Export Issues**:
   
   * Check filters
   * Verify format
   * Test delivery
   * Monitor size
   * Check permissions

2. **Import Issues**:
   
   * Validate data
   * Check mapping
   * Monitor errors
   * Test sample
   * Verify results

3. **Performance Issues**:
   
   * Optimize size
   * Batch process
   * Schedule off-peak
   * Monitor resources
   * Check network

Support
------

For data transfer issues:

1. Check the :doc:`troubleshooting` guide
2. Review transfer documentation
3. Contact support with:
   * Transfer details
   * Error messages
   * Sample data
   * Configuration info 