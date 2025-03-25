Troubleshooting Guide
==================

This guide provides detailed solutions for common issues encountered while using ExpenseDocAI.

Document Processing Issues
----------------------

Failed Document Upload
~~~~~~~~~~~~~~~~~~

**Symptoms:**
- Upload fails with error message
- Document appears stuck in processing
- System returns validation error

**Common Causes:**
1. File size exceeds limit
2. Unsupported file format
3. Corrupted file
4. Network timeout
5. Server capacity issues

**Solutions:**

1. **File Size Issues:**
   
   .. code-block:: python
   
       # Check file size before upload
       def validate_file_size(file_path, max_size_mb=10):
           file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
           return file_size <= max_size_mb

2. **Format Validation:**
   
   .. code-block:: python
   
       # Validate file format
       def validate_format(file_path):
           allowed_formats = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff']
           return any(file_path.lower().endswith(fmt) for fmt in allowed_formats)

3. **File Integrity Check:**
   
   .. code-block:: python
   
       # Verify file integrity
       def check_file_integrity(file_path):
           try:
               with open(file_path, 'rb') as f:
                   # Attempt to read file
                   f.read()
               return True
           except Exception:
               return False

Poor OCR Results
~~~~~~~~~~~~~

**Symptoms:**
- Missing or incorrect text extraction
- Garbled characters
- Incomplete data capture

**Common Causes:**
1. Low image quality
2. Poor document orientation
3. Complex layouts
4. Non-standard fonts
5. Background noise

**Solutions:**

1. **Image Enhancement:**
   
   .. code-block:: python
   
       from PIL import Image, ImageEnhance
       
       def enhance_image(image_path):
           image = Image.open(image_path)
           # Increase contrast
           enhancer = ImageEnhance.Contrast(image)
           image = enhancer.enhance(1.5)
           # Increase sharpness
           enhancer = ImageEnhance.Sharpness(image)
           image = enhancer.enhance(1.5)
           return image

2. **Orientation Correction:**
   
   .. code-block:: python
   
       def correct_orientation(image):
           # Use tesseract to detect orientation
           orientation = pytesseract.image_to_osd(image)
           angle = re.search('(?<=Rotate: )\d+', orientation).group(0)
           # Rotate if needed
           if angle != '0':
               image = image.rotate(int(angle))
           return image

Authentication Issues
-----------------

API Authentication Failures
~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
- 401 Unauthorized errors
- Invalid token messages
- Authentication timeout

**Common Causes:**
1. Expired tokens
2. Invalid credentials
3. Missing headers
4. Rate limiting
5. IP restrictions

**Solutions:**

1. **Token Refresh:**
   
   .. code-block:: python
   
       def refresh_token(refresh_token):
           headers = {'Content-Type': 'application/json'}
           data = {
               'grant_type': 'refresh_token',
               'refresh_token': refresh_token
           }
           response = requests.post(
               'https://api.expensedocai.com/oauth/token',
               headers=headers,
               json=data
           )
           return response.json()

2. **Rate Limit Handling:**
   
   .. code-block:: python
   
       def handle_rate_limit(response):
           if response.status_code == 429:
               retry_after = int(response.headers.get('Retry-After', 60))
               time.sleep(retry_after)
               return True
           return False

Database Issues
------------

Connection Errors
~~~~~~~~~~~~~

**Symptoms:**
- Database timeout errors
- Connection refused messages
- Deadlock errors

**Common Causes:**
1. Network issues
2. Resource exhaustion
3. Configuration errors
4. Connection pool limits
5. Lock contention

**Solutions:**

1. **Connection Retry:**
   
   .. code-block:: python
   
       def get_db_connection(max_retries=3):
           for attempt in range(max_retries):
               try:
                   return database.connect(
                       host=settings.DB_HOST,
                       user=settings.DB_USER,
                       password=settings.DB_PASSWORD,
                       database=settings.DB_NAME
                   )
               except Exception as e:
                   if attempt == max_retries - 1:
                       raise
                   time.sleep(2 ** attempt)

2. **Connection Pool Management:**
   
   .. code-block:: python
   
       from django.db import connection
       
       def reset_db_connection():
           try:
               connection.close()
               connection.connect()
               return True
           except Exception:
               return False

Performance Issues
--------------

Slow Processing
~~~~~~~~~~~~

**Symptoms:**
- Long processing times
- Timeout errors
- High resource usage

**Common Causes:**
1. Large batch sizes
2. Insufficient resources
3. Unoptimized queries
4. Cache misses
5. Background tasks

**Solutions:**

1. **Batch Processing:**
   
   .. code-block:: python
   
       def process_in_batches(items, batch_size=100):
           for i in range(0, len(items), batch_size):
               batch = items[i:i + batch_size]
               try:
                   process_batch(batch)
               except Exception as e:
                   log_error(f"Batch {i//batch_size} failed: {str(e)}")

2. **Query Optimization:**
   
   .. code-block:: python
   
       from django.db.models import Prefetch
       
       def optimize_expense_query():
           return Expense.objects.prefetch_related(
               Prefetch('items'),
               Prefetch('attachments')
           ).select_related('vendor', 'category')

Integration Issues
--------------

API Synchronization
~~~~~~~~~~~~~~~

**Symptoms:**
- Data inconsistencies
- Failed webhooks
- Missing updates

**Common Causes:**
1. Network issues
2. API version mismatch
3. Data format issues
4. Timing problems
5. State conflicts

**Solutions:**

1. **Webhook Retry:**
   
   .. code-block:: python
   
       def retry_webhook(webhook_data, max_retries=3):
           for attempt in range(max_retries):
               try:
                   response = requests.post(
                       webhook_data['url'],
                       json=webhook_data['payload'],
                       headers=webhook_data['headers']
                   )
                   if response.ok:
                       return True
               except Exception:
                   time.sleep(2 ** attempt)
           return False

2. **Data Validation:**
   
   .. code-block:: python
   
       def validate_integration_data(data, schema):
           try:
               jsonschema.validate(instance=data, schema=schema)
               return True
           except jsonschema.exceptions.ValidationError:
               return False

Logging and Monitoring
------------------

1. **Enable Debug Logging:**
   
   .. code-block:: python
   
       import logging
       
       def setup_debug_logging():
           logging.basicConfig(
               level=logging.DEBUG,
               format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
               filename='debug.log'
           )

2. **Monitor System Health:**
   
   .. code-block:: python
   
       def check_system_health():
           checks = {
               'database': check_db_connection(),
               'redis': check_redis_connection(),
               'storage': check_storage_space(),
               'api': check_api_status()
           }
           return all(checks.values()), checks

Recovery Procedures
---------------

1. **Data Recovery:**
   
   .. code-block:: python
   
       def recover_failed_transactions():
           failed_transactions = Transaction.objects.filter(
               status='failed',
               created_at__gte=datetime.now() - timedelta(hours=24)
           )
           for transaction in failed_transactions:
               try:
                   retry_transaction(transaction)
               except Exception as e:
                   log_recovery_error(transaction, str(e))

2. **System Reset:**
   
   .. code-block:: python
   
       def reset_system_state():
           # Clear caches
           cache.clear()
           # Reset connections
           reset_db_connection()
           # Clear temporary files
           clear_temp_files()
           # Restart workers
           restart_celery_workers()

Contact Support
------------

If you're unable to resolve an issue using this guide:

1. Gather relevant information:
   - Error messages
   - Log files
   - System state
   - Steps to reproduce

2. Contact support:
   - Email: support@expensedocai.com
   - Phone: 1-800-EXPENSE
   - Web: https://support.expensedocai.com

3. Include in your report:
   - Account ID
   - Environment details
   - Timeline of issue
   - Impact assessment 