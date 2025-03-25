Integrations Guide
=================

This guide explains how to manage integrations in ExpenseDocAI.

Integration Types
--------------

ExpenseDocAI supports various integration types:

1. **Accounting Systems**
   ~~~~~~~~~~~~~~~~~

   Configure accounting system integrations:

   .. code-block:: json

      {
          "accounting_integration": {
              "system": "quickbooks",
              "version": "online",
              "sync_frequency": "daily",
              "mappings": {
                  "chart_of_accounts": {
                      "travel": "6200",
                      "meals": "6300",
                      "office_supplies": "6400"
                  },
                  "departments": {
                      "sales": "DEPT-001",
                      "engineering": "DEPT-002",
                      "marketing": "DEPT-003"
                  },
                  "classes": {
                      "project_a": "CLASS-001",
                      "project_b": "CLASS-002"
                  }
              }
          }
      }

2. **HR Systems**
   ~~~~~~~~~~

   Configure HR system integrations:

   .. code-block:: json

      {
          "hr_integration": {
              "system": "workday",
              "sync_frequency": "daily",
              "mappings": {
                  "employees": {
                      "fields": [
                          "employee_id",
                          "full_name",
                          "department",
                          "manager",
                          "cost_center"
                      ],
                      "filters": {
                          "status": "active",
                          "type": "full_time"
                      }
                  },
                  "approvers": {
                      "fields": [
                          "employee_id",
                          "approval_level",
                          "departments"
                      ]
                  }
              }
          }
      }

Integration Setup
--------------

Configure integrations through the API:

1. **Create Integration**:

   .. code-block:: python

      def create_integration(integration_data, api_token):
          url = 'http://example.com/api/v1/integrations/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=integration_data
          )
          
          return response.json()

2. **Update Integration**:

   .. code-block:: python

      def update_integration(integration_id, integration_data, api_token):
          url = f'http://example.com/api/v1/integrations/{integration_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.put(
              url,
              headers=headers,
              json=integration_data
          )
          
          return response.json()

Authentication
------------

Manage integration authentication:

1. **OAuth Setup**:

   .. code-block:: python

      def setup_oauth(oauth_data, api_token):
          url = 'http://example.com/api/v1/integrations/oauth/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'integration_id': oauth_data['integration_id'],
                  'client_id': oauth_data['client_id'],
                  'client_secret': oauth_data['client_secret'],
                  'redirect_uri': oauth_data['redirect_uri'],
                  'scope': oauth_data['scope']
              }
          )
          
          return response.json()

2. **API Key Setup**:

   .. code-block:: python

      def setup_api_key(api_key_data, api_token):
          url = 'http://example.com/api/v1/integrations/api-key/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'integration_id': api_key_data['integration_id'],
                  'api_key': api_key_data['api_key'],
                  'api_secret': api_key_data['api_secret']
              }
          )
          
          return response.json()

Data Synchronization
-----------------

Configure data sync settings:

1. **Sync Configuration**:

   .. code-block:: json

      {
          "sync_config": {
              "frequency": "hourly",
              "retry_attempts": 3,
              "retry_delay": 300,
              "notification_email": "admin@example.com",
              "entities": [
                  {
                      "name": "employees",
                      "enabled": true,
                      "sync_type": "incremental",
                      "fields": ["*"]
                  },
                  {
                      "name": "expenses",
                      "enabled": true,
                      "sync_type": "full",
                      "fields": ["id", "amount", "date", "category"]
                  }
              ]
          }
      }

2. **Sync Management**:

   .. code-block:: python

      def manage_sync(sync_data, api_token):
          url = 'http://example.com/api/v1/integrations/sync/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=sync_data
          )
          
          return response.json()

Error Handling
------------

Configure error handling:

1. **Error Configuration**:

   .. code-block:: json

      {
          "error_handling": {
              "retry_policy": {
                  "max_attempts": 3,
                  "delay_seconds": 300,
                  "exponential_backoff": true
              },
              "notifications": {
                  "email": ["admin@example.com"],
                  "slack": "#integration-alerts"
              },
              "error_types": {
                  "authentication": {
                      "action": "notify_admin",
                      "priority": "high"
                  },
                  "data_sync": {
                      "action": "retry",
                      "priority": "medium"
                  }
              }
          }
      }

2. **Error Handling**:

   .. code-block:: python

      def handle_integration_error(error_data, api_token):
          url = 'http://example.com/api/v1/integrations/errors/'
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

Monitoring
---------

Monitor integration health:

1. **Health Checks**:
   
   * Connection status
   * Sync status
   * Error rates
   * Response times
   * Data quality

2. **Metrics Collection**:

   .. code-block:: python

      def collect_metrics(metrics_data, api_token):
          url = 'http://example.com/api/v1/integrations/metrics/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=metrics_data
          )
          
          return response.json()

Best Practices
------------

1. **Integration Setup**:
   
   * Test thoroughly
   * Document configs
   * Monitor health
   * Regular updates
   * Backup data

2. **Security**:
   
   * Secure credentials
   * Audit access
   * Encrypt data
   * Monitor usage
   * Regular reviews

3. **Maintenance**:
   
   * Update mappings
   * Check sync
   * Clean errors
   * Test backups
   * Monitor logs

Troubleshooting
-------------

Common integration issues and solutions:

1. **Connection Issues**:
   
   * Check credentials
   * Verify endpoints
   * Test network
   * Update configs
   * Check logs

2. **Sync Issues**:
   
   * Verify mappings
   * Check data
   * Test sync
   * Clear cache
   * Monitor errors

3. **Performance Issues**:
   
   * Optimize sync
   * Reduce load
   * Update schedule
   * Monitor resources
   * Check bottlenecks

Support
------

For integration issues:

1. Check the :doc:`troubleshooting` guide
2. Review integration documentation
3. Contact support with:
   * Integration details
   * Error messages
   * Log files
   * Configuration data 