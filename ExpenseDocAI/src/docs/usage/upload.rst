Document Upload Guide
==================

This guide explains how to upload documents to ExpenseDocAI.

Supported Formats
--------------

ExpenseDocAI accepts the following file formats:

* **PDF Documents**
  - Single or multi-page PDFs
  - Maximum size: 10MB
  - Text-based or scanned

* **Images**
  - JPEG/JPG (Maximum 10MB)
  - PNG (Maximum 10MB)
  - Minimum resolution: 300 DPI
  - Maximum dimensions: 5000x5000 pixels

Document Requirements
-----------------

For optimal results:

1. **Quality Requirements**
   * Clear, legible text
   * Good lighting and contrast
   * No blurring or distortion
   * Proper orientation
   * Minimal background noise

2. **Content Requirements**
   * Complete expense information
   * Visible date and amount
   * Clear vendor details
   * Readable line items
   * Visible tax information

3. **Size Requirements**
   * File size: 1-10MB
   * Resolution: 300+ DPI
   * Dimensions: 500-5000 pixels

Upload Methods
-----------

1. **API Upload**

   Basic upload using Python:

   .. code-block:: python

      import requests

      def upload_document(file_path, api_key):
          headers = {'Authorization': f'Bearer {api_key}'}
          
          with open(file_path, 'rb') as f:
              files = {'file': f}
              response = requests.post(
                  'https://api.expensedocai.com/api/v1/documents/',
                  headers=headers,
                  files=files
              )
          
          return response.json()

2. **Batch Upload**

   Upload multiple documents:

   .. code-block:: python

      def batch_upload(file_paths, api_key):
          results = []
          for path in file_paths:
              try:
                  result = upload_document(path, api_key)
                  results.append(result)
              except Exception as e:
                  results.append({'error': str(e), 'file': path})
          return results

3. **Upload with Metadata**

   Include additional information:

   .. code-block:: python

      def upload_with_metadata(file_path, metadata, api_key):
          headers = {
              'Authorization': f'Bearer {api_key}',
              'Content-Type': 'multipart/form-data'
          }
          
          with open(file_path, 'rb') as f:
              files = {'file': f}
              data = {
                  'metadata': metadata,
                  'options': {
                      'validate': True,
                      'async': False
                  }
              }
              response = requests.post(
                  'https://api.expensedocai.com/api/v1/documents/',
                  headers=headers,
                  files=files,
                  data=data
              )
          
          return response.json()

Upload Options
-----------

Configure uploads with these options:

1. **Validation Options**
   * ``validate``: Enable/disable validation
   * ``validation_level``: Basic or strict
   * ``validation_rules``: Custom rules

2. **Processing Options**
   * ``async``: Async or sync processing
   * ``priority``: Processing priority
   * ``callback_url``: Webhook URL

3. **Metadata Options**
   * ``category``: Expense category
   * ``description``: Description
   * ``tags``: Custom tags
   * ``custom_fields``: Additional fields

Example configuration:

.. code-block:: python

   options = {
       'validate': True,
       'validation_level': 'strict',
       'async': True,
       'priority': 'high',
       'callback_url': 'https://your-domain.com/webhook',
       'metadata': {
           'category': 'travel',
           'description': 'Business trip expenses',
           'tags': ['urgent', 'travel'],
           'custom_fields': {
               'department': 'sales',
               'project': 'client-visit'
           }
       }
   }

Validation Rules
-------------

ExpenseDocAI validates uploads against these rules:

1. **File Validation**
   * Format check
   * Size limits
   * Resolution requirements
   * Quality thresholds

2. **Content Validation**
   * Required fields
   * Date formats
   * Amount formats
   * Vendor information

3. **Metadata Validation**
   * Required metadata
   * Format checks
   * Value constraints
   * Relationship rules

Example validation configuration:

.. code-block:: python

   validation_rules = {
       'required_fields': ['date', 'amount', 'vendor'],
       'amount_format': '^\\d+\\.\\d{2}$',
       'date_format': '%Y-%m-%d',
       'vendor_required': True,
       'metadata_rules': {
           'category': ['travel', 'meals', 'office'],
           'amount_max': 10000,
           'require_description': True
       }
   }

Error Handling
-----------

Common upload errors and solutions:

1. **File Errors**
   * Error: "File too large"
   * Solution: Compress file

2. **Format Errors**
   * Error: "Invalid format"
   * Solution: Convert to supported format

3. **Validation Errors**
   * Error: "Missing required fields"
   * Solution: Check document completeness

4. **API Errors**
   * Error: "Authentication failed"
   * Solution: Verify API key

Handle errors in code:

.. code-block:: python

   def handle_upload_error(error_response):
       error = error_response.json()
       
       if error['error'] == 'file_error':
           if 'size' in error['details']:
               compress_and_retry()
           elif 'format' in error['details']:
               convert_and_retry()
       
       elif error['error'] == 'validation_error':
           fix_validation_issues()
       
       return error['message']

Best Practices
------------

1. **File Preparation**
   * Optimize file size
   * Check format compatibility
   * Verify content quality
   * Remove sensitive data

2. **Upload Strategy**
   * Batch similar documents
   * Use async for large batches
   * Implement retry logic
   * Monitor upload status

3. **Error Management**
   * Handle errors gracefully
   * Implement retries
   * Log upload issues
   * Monitor success rates

4. **Performance**
   * Compress large files
   * Use appropriate formats
   * Monitor upload times
   * Implement rate limiting

Integration Examples
-----------------

1. **Basic Integration**:

   .. code-block:: python

      def simple_upload_flow(file_path, api_key):
          # Prepare file
          optimized_file = optimize_file(file_path)
          
          # Upload
          try:
              result = upload_document(optimized_file, api_key)
              return result
          except Exception as e:
              handle_upload_error(e)

2. **Advanced Integration**:

   .. code-block:: python

      def advanced_upload_flow(file_path, metadata, api_key):
          # Validate file
          if not validate_file(file_path):
              return {'error': 'Invalid file'}
          
          # Prepare options
          options = prepare_upload_options(metadata)
          
          # Upload with retry
          max_retries = 3
          for attempt in range(max_retries):
              try:
                  result = upload_with_metadata(
                      file_path,
                      metadata,
                      api_key
                  )
                  return result
              except Exception as e:
                  if attempt == max_retries - 1:
                      raise e
                  time.sleep(2 ** attempt)

3. **Batch Integration**:

   .. code-block:: python

      def batch_upload_flow(file_paths, metadata_list, api_key):
          results = []
          for file_path, metadata in zip(file_paths, metadata_list):
              try:
                  result = advanced_upload_flow(
                      file_path,
                      metadata,
                      api_key
                  )
                  results.append(result)
              except Exception as e:
                  results.append({
                      'error': str(e),
                      'file': file_path
                  })
          return results

Support
------

For upload issues:

1. Check file requirements
2. Verify API credentials
3. Review error messages
4. Contact support:
   * Email: support@expensedocai.com
   * Phone: 1-800-EXPENSE
   * Web: https://support.expensedocai.com 