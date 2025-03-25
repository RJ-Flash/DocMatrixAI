Document Processing Guide
======================

This guide explains how ExpenseDocAI processes expense documents and extracts information.

Processing Overview
----------------

ExpenseDocAI uses advanced AI models to process expense documents through several stages:

1. **Document Upload**
   * Files are uploaded via API or web interface
   * Initial validation checks format and size
   * Document is queued for processing

2. **Image Preprocessing**
   * Convert documents to standard format
   * Enhance image quality if needed
   * Correct orientation
   * Remove noise and artifacts

3. **OCR Processing**
   * Extract text using OCR
   * Identify text regions and layout
   * Map spatial relationships
   * Calculate confidence scores

4. **Data Extraction**
   * Identify key fields:
     - Date
     - Amount
     - Vendor
     - Items
     - Tax
   * Apply field-specific validation
   * Calculate confidence scores

5. **Policy Validation**
   * Check against expense policies
   * Identify violations
   * Apply category rules
   * Validate amounts and limits

6. **Result Generation**
   * Create structured data output
   * Generate confidence scores
   * Prepare webhook notifications
   * Store results

Processing Status
--------------

Documents can have the following status values:

* ``pending``: Document uploaded, waiting for processing
* ``processing``: Document is being processed
* ``completed``: Processing completed successfully
* ``error``: Processing failed

Monitor processing status via API:

.. code-block:: python

   import requests

   def check_status(document_id, api_key):
       headers = {'Authorization': f'Bearer {api_key}'}
       response = requests.get(
           f'https://api.expensedocai.com/api/v1/documents/{document_id}/',
           headers=headers
       )
       return response.json()['status']

Webhook Notifications
------------------

Configure webhooks to receive real-time updates:

.. code-block:: python

   def configure_webhook(api_key, webhook_url):
       headers = {
           'Authorization': f'Bearer {api_key}',
           'Content-Type': 'application/json'
       }
       data = {
           'url': webhook_url,
           'events': ['document.completed', 'document.error'],
           'active': True
       }
       response = requests.post(
           'https://api.expensedocai.com/api/v1/webhooks/',
           headers=headers,
           json=data
       )
       return response.json()

Webhook events:

* ``document.uploaded``: Document upload completed
* ``document.processing``: Processing started
* ``document.completed``: Processing completed successfully
* ``document.error``: Processing failed

Error Handling
-----------

Common processing errors:

1. **Poor Image Quality**
   * Error: "Unable to extract text"
   * Solution: Upload clearer image

2. **Invalid Format**
   * Error: "Unsupported file type"
   * Solution: Convert to supported format

3. **Missing Information**
   * Error: "Required fields not found"
   * Solution: Check document completeness

4. **Processing Timeout**
   * Error: "Processing exceeded time limit"
   * Solution: Retry with optimized file

Handle errors in your code:

.. code-block:: python

   def handle_processing_error(error_response):
       error = error_response.json()
       if error['error'] == 'processing_error':
           if 'quality' in error['details']:
               # Handle image quality issues
               enhance_and_reupload()
           elif 'timeout' in error['details']:
               # Handle timeout
               retry_with_optimization()
       return error['message']

Best Practices
------------

1. **Document Preparation**
   * Use high-quality scans (300+ DPI)
   * Ensure good lighting
   * Keep documents flat
   * Remove unnecessary content

2. **Processing Strategy**
   * Batch similar documents
   * Monitor processing status
   * Handle errors appropriately
   * Implement retry logic

3. **Performance Optimization**
   * Compress large files
   * Use appropriate formats
   * Monitor processing times
   * Implement rate limiting

4. **Error Management**
   * Log processing errors
   * Implement retry logic
   * Monitor error rates
   * Update error handling

Integration Examples
-----------------

1. **Basic Processing**:

   .. code-block:: python

      def process_document(file_path, api_key):
          # Upload document
          with open(file_path, 'rb') as f:
              response = requests.post(
                  'https://api.expensedocai.com/api/v1/documents/',
                  headers={'Authorization': f'Bearer {api_key}'},
                  files={'file': f}
              )
          
          document = response.json()
          
          # Monitor processing
          while True:
              status = check_status(document['id'], api_key)
              if status in ['completed', 'error']:
                  break
              time.sleep(5)
          
          return document

2. **Batch Processing**:

   .. code-block:: python

      def batch_process(file_paths, api_key):
          results = []
          for path in file_paths:
              try:
                  result = process_document(path, api_key)
                  results.append(result)
              except Exception as e:
                  results.append({'error': str(e), 'file': path})
          return results

3. **Webhook Integration**:

   .. code-block:: python

      from flask import Flask, request

      app = Flask(__name__)

      @app.route('/webhook', methods=['POST'])
      def handle_webhook():
          event = request.json
          
          if event['event'] == 'document.completed':
              process_completed_document(event['data'])
          elif event['event'] == 'document.error':
              handle_processing_error(event['data'])
          
          return '', 200

Support
------

For processing issues:

1. Check the error message
2. Review document quality
3. Verify API credentials
4. Contact support if needed:
   * Email: support@expensedocai.com
   * Phone: 1-800-EXPENSE
   * Web: https://support.expensedocai.com 