Notifications and Alerts Guide
=========================

This guide explains how to manage notifications and alerts in ExpenseDocAI.

Notification Types
---------------

ExpenseDocAI supports various notification types:

1. **System Notifications**
   ~~~~~~~~~~~~~~~~~~~

   Configure system-level notifications:

   .. code-block:: json

      {
          "system_notifications": {
              "maintenance": {
                  "enabled": true,
                  "advance_notice": "24h",
                  "channels": ["email", "in_app"],
                  "recipients": ["all_users"]
              },
              "updates": {
                  "enabled": true,
                  "frequency": "weekly",
                  "channels": ["email", "in_app"],
                  "recipients": ["admins"]
              },
              "alerts": {
                  "enabled": true,
                  "severity_levels": ["critical", "warning", "info"],
                  "channels": ["email", "slack", "sms"],
                  "recipients": ["system_admins"]
              }
          }
      }

2. **User Notifications**
   ~~~~~~~~~~~~~~~~~

   Configure user-specific notifications:

   .. code-block:: json

      {
          "user_notifications": {
              "expense_submission": {
                  "enabled": true,
                  "events": [
                      "submitted",
                      "approved",
                      "rejected",
                      "requires_revision"
                  ],
                  "channels": ["email", "in_app"]
              },
              "approvals": {
                  "enabled": true,
                  "events": [
                      "pending_approval",
                      "approved",
                      "rejected",
                      "delegated"
                  ],
                  "channels": ["email", "in_app", "mobile"]
              },
              "reminders": {
                  "enabled": true,
                  "types": [
                      "pending_submission",
                      "pending_approval",
                      "policy_violation"
                  ],
                  "frequency": "daily"
              }
          }
      }

Notification Configuration
----------------------

Configure notifications through the API:

1. **Create Notification**:

   .. code-block:: python

      def create_notification(notification_data, api_token):
          url = 'http://example.com/api/v1/notifications/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=notification_data
          )
          
          return response.json()

2. **Update Notification**:

   .. code-block:: python

      def update_notification(notification_id, notification_data, api_token):
          url = f'http://example.com/api/v1/notifications/{notification_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.put(
              url,
              headers=headers,
              json=notification_data
          )
          
          return response.json()

Channel Configuration
-----------------

Configure notification channels:

1. **Email Settings**:

   .. code-block:: json

      {
          "email_config": {
              "smtp_settings": {
                  "host": "smtp.example.com",
                  "port": 587,
                  "username": "notifications@example.com",
                  "use_tls": true
              },
              "templates": {
                  "expense_submitted": {
                      "subject": "New Expense Submission",
                      "template_id": "exp_sub_001"
                  },
                  "approval_required": {
                      "subject": "Approval Required",
                      "template_id": "apr_req_001"
                  }
              },
              "throttling": {
                  "max_per_hour": 100,
                  "max_per_user": 10
              }
          }
      }

2. **Slack Integration**:

   .. code-block:: python

      def configure_slack(slack_config, api_token):
          url = 'http://example.com/api/v1/notifications/channels/slack/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'webhook_url': slack_config['webhook_url'],
                  'default_channel': slack_config['default_channel'],
                  'username': slack_config['username'],
                  'icon_emoji': slack_config['icon_emoji']
              }
          )
          
          return response.json()

Alert Management
-------------

Configure and manage alerts:

1. **Alert Rules**:

   .. code-block:: json

      {
          "alert_rules": {
              "expense_threshold": {
                  "condition": "amount > 5000",
                  "severity": "high",
                  "notification": {
                      "channels": ["email", "slack"],
                      "recipients": ["finance_team"]
                  }
              },
              "policy_violation": {
                  "condition": "violations > 3",
                  "severity": "medium",
                  "notification": {
                      "channels": ["email"],
                      "recipients": ["manager", "compliance"]
                  }
              },
              "system_health": {
                  "condition": "error_rate > 5%",
                  "severity": "critical",
                  "notification": {
                      "channels": ["email", "sms"],
                      "recipients": ["system_admin"]
                  }
              }
          }
      }

2. **Alert Processing**:

   .. code-block:: python

      def process_alert(alert_data, api_token):
          url = 'http://example.com/api/v1/alerts/process/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'type': alert_data['type'],
                  'severity': alert_data['severity'],
                  'message': alert_data['message'],
                  'metadata': alert_data['metadata']
              }
          )
          
          return response.json()

Template Management
----------------

Manage notification templates:

1. **Template Configuration**:

   .. code-block:: python

      def configure_template(template_data, api_token):
          url = 'http://example.com/api/v1/notifications/templates/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'name': template_data['name'],
                  'type': template_data['type'],
                  'subject': template_data['subject'],
                  'body': template_data['body'],
                  'variables': template_data['variables']
              }
          )
          
          return response.json()

2. **Template Variables**:

   .. code-block:: json

      {
          "template_variables": {
              "expense": [
                  "{{expense_id}}",
                  "{{amount}}",
                  "{{category}}",
                  "{{submitter}}",
                  "{{date}}"
              ],
              "approval": [
                  "{{approver}}",
                  "{{status}}",
                  "{{comments}}",
                  "{{due_date}}"
              ],
              "system": [
                  "{{alert_type}}",
                  "{{severity}}",
                  "{{timestamp}}",
                  "{{details}}"
              ]
          }
      }

Best Practices
------------

1. **Notification Design**:
   
   * Clear purpose
   * Relevant content
   * Proper timing
   * Right channel
   * User preferences

2. **Alert Configuration**:
   
   * Meaningful triggers
   * Appropriate severity
   * Clear actions
   * Proper routing
   * Avoid noise

3. **Template Management**:
   
   * Consistent style
   * Clear formatting
   * Variable validation
   * Regular updates
   * Version control

Troubleshooting
-------------

Common notification issues and solutions:

1. **Delivery Issues**:
   
   * Check settings
   * Verify channels
   * Test templates
   * Monitor logs
   * Check filters

2. **Template Issues**:
   
   * Validate syntax
   * Check variables
   * Test rendering
   * Update content
   * Fix formatting

3. **Alert Issues**:
   
   * Verify rules
   * Check conditions
   * Test triggers
   * Update thresholds
   * Monitor frequency

Support
------

For notification issues:

1. Check the :doc:`troubleshooting` guide
2. Review notification documentation
3. Contact support with:
   * Notification details
   * Error messages
   * Template data
   * Configuration info 