Quickstart Guide
==============

This guide will help you get started with ExpenseDocAI quickly. We'll cover the basics of uploading documents, processing them, and retrieving the extracted data.

Prerequisites
------------

Before starting, ensure you have:

* Completed the :doc:`installation` process
* Created a superuser account
* Started the development server
* Access to the API endpoints

Authentication
-------------

First, obtain an authentication token:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "your_username", "password": "your_password"}'

The response will contain your token:

.. code-block:: json

   {
       "token": "your-auth-token"
   }

Use this token in subsequent requests by including it in the Authorization header:

.. code-block:: bash

   Authorization: Token your-auth-token

Uploading Documents
-----------------

To upload an expense document:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/documents/ \
        -H "Authorization: Token your-auth-token" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@path/to/your/receipt.pdf" \
        -F "process_now=true"

The response will include the document ID and status:

.. code-block:: json

   {
       "id": "123",
       "status": "processing",
       "file_url": "http://localhost:8000/media/documents/receipt.pdf",
       "uploaded_at": "2024-01-25T12:00:00Z"
   }

Checking Processing Status
------------------------

To check the status of a document:

.. code-block:: bash

   curl http://localhost:8000/api/v1/documents/123/ \
        -H "Authorization: Token your-auth-token"

The response will show the current status:

.. code-block:: json

   {
       "id": "123",
       "status": "completed",
       "entries": [
           {
               "amount": "123.45",
               "currency": "USD",
               "date": "2024-01-25",
               "vendor": "Office Supplies Inc",
               "category": "office_supplies",
               "confidence_score": 0.95
           }
       ]
   }

Retrieving Expense Entries
------------------------

To list all expense entries:

.. code-block:: bash

   curl http://localhost:8000/api/v1/entries/ \
        -H "Authorization: Token your-auth-token"

To get a specific entry:

.. code-block:: bash

   curl http://localhost:8000/api/v1/entries/456/ \
        -H "Authorization: Token your-auth-token"

Python Client Example
-------------------

Here's a complete example using Python:

.. code-block:: python

   import requests
   
   # Configuration
   BASE_URL = 'http://localhost:8000/api/v1'
   TOKEN = 'your-auth-token'
   HEADERS = {'Authorization': f'Token {TOKEN}'}
   
   # Upload document
   with open('receipt.pdf', 'rb') as f:
       response = requests.post(
           f'{BASE_URL}/documents/',
           headers=HEADERS,
           files={'file': f},
           data={'process_now': True}
       )
   
   document_id = response.json()['id']
   
   # Check status
   while True:
       response = requests.get(
           f'{BASE_URL}/documents/{document_id}/',
           headers=HEADERS
       )
       status = response.json()['status']
       
       if status == 'completed':
           entries = response.json()['entries']
           break
       elif status == 'failed':
           print('Processing failed')
           break
   
   # Print results
   for entry in entries:
       print(f"Amount: {entry['amount']} {entry['currency']}")
       print(f"Date: {entry['date']}")
       print(f"Vendor: {entry['vendor']}")
       print(f"Category: {entry['category']}")
       print(f"Confidence: {entry['confidence_score']}")
       print("---")

Error Handling
------------

The API uses standard HTTP status codes:

* 200: Success
* 201: Created
* 400: Bad Request
* 401: Unauthorized
* 403: Forbidden
* 404: Not Found
* 500: Server Error

Error responses include detailed messages:

.. code-block:: json

   {
       "error": "validation_error",
       "message": "Invalid file format. Supported formats: PDF, JPG, PNG",
       "details": {
           "file": ["File type not supported"]
       }
   }

Next Steps
---------

Now that you're familiar with the basics, you can:

* Explore the :doc:`usage/api` for detailed API documentation
* Learn about :doc:`usage/policies` for expense policy configuration
* Set up :doc:`development/monitoring` for production use
* Check out :doc:`development/testing` for writing tests

Need Help?
---------

If you have questions or need assistance:

* Join our community Discord
* Check our FAQ
* Contact support at support@docmatrixai.com 