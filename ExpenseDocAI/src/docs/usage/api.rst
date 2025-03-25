API Documentation
================

This document provides detailed information about the ExpenseDocAI REST API endpoints.

Version Information
----------------

Current API version: v1
Base URL: ``https://api.expensedocai.com/api/v1/``

All API requests should include the version in the URL path. Future versions will be announced with appropriate migration guides and deprecation notices.

Authentication
-------------

The API uses JWT (JSON Web Token) based authentication. All requests (except authentication) must include an ``Authorization`` header:

.. code-block:: bash

   Authorization: Bearer <your-token>

To obtain a token:

.. code-block:: bash

   POST /api/v1/auth/token/
   Content-Type: application/json

   {
       "username": "your_username",
       "password": "your_password"
   }

Response:

.. code-block:: json

   {
       "access": "your-access-token",
       "refresh": "your-refresh-token",
       "expires_in": 3600,
       "token_type": "Bearer"
   }

To refresh an expired token:

.. code-block:: bash

   POST /api/v1/auth/token/refresh/
   Content-Type: application/json

   {
       "refresh": "your-refresh-token"
   }

Token Security:
* Access tokens expire after 1 hour
* Refresh tokens expire after 30 days
* Store tokens securely (e.g., encrypted storage)
* Never expose tokens in URLs or logs
* Implement token rotation for security

Documents API
------------

Upload Document
~~~~~~~~~~~~~

Upload an expense document for processing.

.. code-block:: bash

   POST /api/v1/documents/
   Content-Type: multipart/form-data

Parameters:

* ``file`` (required): The document file (PDF, JPG, PNG)
* ``process_now`` (optional): Boolean to process immediately (default: true)

Response:

.. code-block:: json

   {
       "id": "123",
       "status": "processing",
       "file_url": "http://example.com/media/documents/receipt.pdf",
       "file_type": "pdf",
       "uploaded_at": "2024-02-20T12:00:00Z",
       "processing_started_at": "2024-02-20T12:00:01Z",
       "processing_completed_at": null,
       "error_message": null
   }

List Documents
~~~~~~~~~~~~

Retrieve a list of uploaded documents.

.. code-block:: bash

   GET /api/v1/documents/

Parameters:

* ``status`` (optional): Filter by status (pending, processing, completed, error)
* ``page`` (optional): Page number for pagination
* ``page_size`` (optional): Number of items per page

Response:

.. code-block:: json

   {
       "count": 100,
       "next": "http://example.com/api/v1/documents/?page=2",
       "previous": null,
       "results": [
           {
               "id": "123",
               "status": "completed",
               "file_url": "http://example.com/media/documents/receipt.pdf",
               "file_type": "pdf",
               "uploaded_at": "2024-02-20T12:00:00Z",
               "entries": [...]
           }
       ]
   }

Get Document
~~~~~~~~~~

Retrieve a specific document by ID.

.. code-block:: bash

   GET /api/v1/documents/{id}/

Response:

.. code-block:: json

   {
       "id": "123",
       "status": "completed",
       "file_url": "http://example.com/media/documents/receipt.pdf",
       "file_type": "pdf",
       "uploaded_at": "2024-02-20T12:00:00Z",
       "processing_started_at": "2024-02-20T12:00:01Z",
       "processing_completed_at": "2024-02-20T12:00:10Z",
       "error_message": null,
       "entries": [
           {
               "id": "456",
               "amount": "123.45",
               "currency": "USD",
               "date": "2024-02-20",
               "vendor": "Office Supplies Inc",
               "category": "office_supplies",
               "description": "Office supplies purchase",
               "tax_amount": "10.00",
               "confidence_score": 0.95,
               "policy_violations": []
           }
       ]
   }

Delete Document
~~~~~~~~~~~~

Delete a specific document.

.. code-block:: bash

   DELETE /api/v1/documents/{id}/

Entries API
----------

List Entries
~~~~~~~~~~

Retrieve a list of expense entries.

.. code-block:: bash

   GET /api/v1/entries/

Parameters:

* ``document`` (optional): Filter by document ID
* ``vendor`` (optional): Filter by vendor name
* ``category`` (optional): Filter by expense category
* ``min_amount`` (optional): Filter by minimum amount
* ``max_amount`` (optional): Filter by maximum amount
* ``start_date`` (optional): Filter by start date
* ``end_date`` (optional): Filter by end date
* ``page`` (optional): Page number for pagination
* ``page_size`` (optional): Number of items per page

Response:

.. code-block:: json

   {
       "count": 50,
       "next": "http://example.com/api/v1/entries/?page=2",
       "previous": null,
       "results": [
           {
               "id": "456",
               "document": "123",
               "amount": "123.45",
               "currency": "USD",
               "date": "2024-02-20",
               "vendor": "Office Supplies Inc",
               "category": "office_supplies",
               "description": "Office supplies purchase",
               "tax_amount": "10.00",
               "confidence_score": 0.95,
               "policy_violations": [],
               "created_at": "2024-02-20T12:00:10Z",
               "updated_at": "2024-02-20T12:00:10Z"
           }
       ]
   }

Get Entry
~~~~~~~~

Retrieve a specific expense entry by ID.

.. code-block:: bash

   GET /api/v1/entries/{id}/

Response:

.. code-block:: json

   {
       "id": "456",
       "document": {
           "id": "123",
           "file_url": "http://example.com/media/documents/receipt.pdf"
       },
       "amount": "123.45",
       "currency": "USD",
       "date": "2024-02-20",
       "vendor": "Office Supplies Inc",
       "category": "office_supplies",
       "description": "Office supplies purchase",
       "tax_amount": "10.00",
       "confidence_score": 0.95,
       "policy_violations": [],
       "created_at": "2024-02-20T12:00:10Z",
       "updated_at": "2024-02-20T12:00:10Z"
   }

Error Handling
------------

The API uses standard HTTP status codes and returns detailed error messages:

* ``200 OK``: Request successful
* ``201 Created``: Resource created successfully
* ``400 Bad Request``: Invalid request parameters
* ``401 Unauthorized``: Missing or invalid authentication
* ``403 Forbidden``: Insufficient permissions
* ``404 Not Found``: Resource not found
* ``500 Internal Server Error``: Server error

Error Response Format:

.. code-block:: json

   {
       "error": "error_code",
       "message": "Human-readable error message",
       "details": {
           "field": ["Specific field error"]
       }
   }

Common error codes:

* ``validation_error``: Invalid input data
* ``authentication_error``: Authentication failed
* ``permission_error``: Insufficient permissions
* ``not_found``: Resource not found
* ``processing_error``: Document processing failed

Rate Limiting
-----------

The API implements rate limiting to ensure fair usage:

* Anonymous users: 100 requests per day
* Authenticated users: 1000 requests per day

Rate limit headers are included in all responses:

.. code-block:: bash

   X-RateLimit-Limit: 1000
   X-RateLimit-Remaining: 995
   X-RateLimit-Reset: 1613846400

When rate limit is exceeded:

.. code-block:: json

   {
       "error": "rate_limit_exceeded",
       "message": "Rate limit exceeded. Please try again later.",
       "details": {
           "retry_after": 3600
       }
   }

Webhooks
-------

Configure webhooks to receive notifications about document processing:

.. code-block:: bash

   POST /api/v1/webhooks/
   Content-Type: application/json

   {
       "url": "https://your-server.com/webhook",
       "events": ["document.completed", "document.error"],
       "secret": "your-webhook-secret",
       "description": "Production webhook endpoint",
       "active": true,
       "retry_config": {
           "max_attempts": 3,
           "backoff_factor": 2
       }
   }

Webhook Security:
* Use HTTPS endpoints only
* Verify webhook signatures
* Implement retry with backoff
* Monitor webhook health
* Handle webhook timeouts

Webhook Events:
* ``document.uploaded``: Document upload completed
* ``document.processing``: Processing started
* ``document.completed``: Processing completed successfully
* ``document.error``: Processing failed
* ``entry.created``: New expense entry created
* ``entry.updated``: Expense entry updated
* ``policy.violation``: Policy violation detected

Webhook payload example:

.. code-block:: json

   {
       "event": "document.completed",
       "timestamp": "2024-02-20T12:00:10Z",
       "webhook_id": "whk_123",
       "signature": "sha256=...",
       "data": {
           "document_id": "123",
           "status": "completed",
           "processing_time": 10.5,
           "entries": [...]
       }
   }

Verify webhook signatures:

.. code-block:: python

   import hmac
   import hashlib

   def verify_webhook_signature(payload, signature, secret):
       expected = hmac.new(
           secret.encode('utf-8'),
           payload.encode('utf-8'),
           hashlib.sha256
       ).hexdigest()
       return hmac.compare_digest(signature, f"sha256={expected}")

SDK Support
---------

Official Python SDK:

.. code-block:: bash

   pip install expensedocai-python

Usage example:

.. code-block:: python

   from expensedocai import Client

   client = Client(api_key='your-api-key')

   # Upload document
   with open('receipt.pdf', 'rb') as f:
       document = client.documents.create(file=f)

   # Get document status
   status = client.documents.get(document.id)

   # List entries
   entries = client.entries.list(
       start_date='2024-01-01',
       end_date='2024-12-31'
   )

Other supported languages:
* JavaScript/Node.js
* Java
* C#
* Go
* Ruby

Security Best Practices
-------------------

1. **API Authentication**:
   * Use strong passwords
   * Implement MFA where possible
   * Rotate tokens regularly
   * Monitor failed attempts
   * Implement IP whitelisting

2. **Data Protection**:
   * Use HTTPS only
   * Encrypt sensitive data
   * Implement data masking
   * Regular security audits
   * Monitor API access

3. **Error Handling**:
   * Don't expose internal errors
   * Log security events
   * Rate limit error responses
   * Implement circuit breakers
   * Monitor error patterns

4. **Access Control**:
   * Implement role-based access
   * Principle of least privilege
   * Regular access reviews
   * Audit logging
   * Session management

5. **API Security**:
   * Input validation
   * Output encoding
   * Content-Security-Policy
   * CORS configuration
   * API versioning

Performance Optimization
--------------------

1. **Caching**:
   * Use Redis for caching
   * Implement ETags
   * Cache-Control headers
   * Conditional requests
   * Cache invalidation

2. **Request Optimization**:
   * Batch operations
   * Pagination
   * Field filtering
   * Compression
   * Connection pooling

3. **Response Optimization**:
   * Minimize payload size
   * GZIP compression
   * Async processing
   * Background jobs
   * Response streaming

4. **Monitoring**:
   * Response times
   * Error rates
   * Cache hit rates
   * API usage patterns
   * Resource utilization

Development Tools
--------------

1. **API Testing**:
   * Postman collection available
   * OpenAPI specification
   * Test environment
   * Sample data
   * Mock responses

2. **Documentation**:
   * Interactive API docs
   * Code examples
   * SDKs and libraries
   * Migration guides
   * Change logs

3. **Development Support**:
   * Developer portal
   * API status page
   * Support channels
   * Feature requests
   * Bug reporting

Appendix
-------

1. **Status Codes**:
   * ``200``: Success
   * ``201``: Created
   * ``202``: Accepted
   * ``204``: No Content
   * ``400``: Bad Request
   * ``401``: Unauthorized
   * ``403``: Forbidden
   * ``404``: Not Found
   * ``409``: Conflict
   * ``422``: Unprocessable Entity
   * ``429``: Too Many Requests
   * ``500``: Internal Server Error
   * ``503``: Service Unavailable

2. **Rate Limits**:
   * Anonymous: 100/day
   * Basic: 1,000/day
   * Premium: 10,000/day
   * Enterprise: Custom limits

3. **File Requirements**:
   * Max file size: 10MB
   * Supported formats: PDF, JPG, PNG
   * Max resolution: 5000x5000
   * Min resolution: 300 DPI

4. **Support**:
   * Email: api-support@expensedocai.com
   * Status: status.expensedocai.com
   * Docs: docs.expensedocai.com
   * GitHub: github.com/expensedocai 