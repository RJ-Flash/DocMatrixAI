User Preferences Guide
===================

This guide explains how to manage user preferences and settings in ExpenseDocAI.

Preference Types
-------------

ExpenseDocAI supports various preference types:

1. **User Settings**
   ~~~~~~~~~~~~~

   Configure user-specific settings:

   .. code-block:: json

      {
          "user_settings": {
              "profile": {
                  "language": "en",
                  "timezone": "UTC",
                  "date_format": "YYYY-MM-DD",
                  "currency": "USD",
                  "number_format": {
                      "decimal_separator": ".",
                      "thousands_separator": ","
                  }
              },
              "notifications": {
                  "email": {
                      "enabled": true,
                      "digest": "daily",
                      "types": [
                          "expense_approved",
                          "expense_rejected",
                          "requires_action"
                      ]
                  },
                  "mobile": {
                      "enabled": true,
                      "quiet_hours": {
                          "start": "22:00",
                          "end": "07:00"
                      }
                  },
                  "in_app": {
                      "enabled": true,
                      "sound": true,
                      "desktop": true
                  }
              }
          }
      }

2. **Display Preferences**
   ~~~~~~~~~~~~~~~~~~

   Configure interface preferences:

   .. code-block:: json

      {
          "display_preferences": {
              "theme": {
                  "mode": "auto",
                  "color": "blue",
                  "contrast": "normal"
              },
              "layout": {
                  "sidebar": "expanded",
                  "density": "comfortable",
                  "font_size": "medium"
              },
              "dashboard": {
                  "default_view": "summary",
                  "widgets": [
                      "recent_expenses",
                      "pending_approvals",
                      "monthly_summary",
                      "policy_alerts"
                  ],
                  "widget_layout": "grid"
              }
          }
      }

Preference Management
------------------

Manage preferences through the API:

1. **Get Preferences**:

   .. code-block:: python

      def get_preferences(user_id, api_token):
          url = f'http://example.com/api/v1/preferences/{user_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.get(
              url,
              headers=headers
          )
          
          return response.json()

2. **Update Preferences**:

   .. code-block:: python

      def update_preferences(user_id, preference_data, api_token):
          url = f'http://example.com/api/v1/preferences/{user_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.put(
              url,
              headers=headers,
              json=preference_data
          )
          
          return response.json()

Default Configuration
------------------

Configure organization-wide defaults:

1. **Default Settings**:

   .. code-block:: json

      {
          "default_settings": {
              "expense_defaults": {
                  "currency": "USD",
                  "category": "uncategorized",
                  "tax_rate": 0.0,
                  "requires_receipt": true
              },
              "approval_defaults": {
                  "auto_approve_threshold": 50.00,
                  "require_notes": false,
                  "allow_delegation": true
              },
              "notification_defaults": {
                  "email_enabled": true,
                  "mobile_enabled": false,
                  "digest_frequency": "daily"
              }
          }
      }

2. **Default Management**:

   .. code-block:: python

      def manage_defaults(default_data, api_token):
          url = 'http://example.com/api/v1/preferences/defaults/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=default_data
          )
          
          return response.json()

Preference Validation
------------------

Validate user preferences:

1. **Validation Rules**:

   .. code-block:: json

      {
          "validation_rules": {
              "language": {
                  "type": "string",
                  "allowed": ["en", "es", "fr", "de", "ja"],
                  "required": true
              },
              "timezone": {
                  "type": "string",
                  "pattern": "^[A-Za-z]+/[A-Za-z_]+$",
                  "required": true
              },
              "currency": {
                  "type": "string",
                  "length": 3,
                  "required": true
              },
              "notification_types": {
                  "type": "array",
                  "min_items": 1,
                  "unique_items": true
              }
          }
      }

2. **Validation Process**:

   .. code-block:: python

      def validate_preferences(preference_data, api_token):
          url = 'http://example.com/api/v1/preferences/validate/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=preference_data
          )
          
          return response.json()

Preference Migration
-----------------

Handle preference migrations:

1. **Migration Configuration**:

   .. code-block:: json

      {
          "migration_config": {
              "version": "2.0.0",
              "rules": [
                  {
                      "from_version": "1.x",
                      "transforms": [
                          {
                              "field": "notification_settings",
                              "action": "rename",
                              "new_name": "notifications"
                          },
                          {
                              "field": "theme.dark_mode",
                              "action": "move",
                              "new_path": "theme.mode"
                          }
                      ]
                  }
              ],
              "backup": true,
              "auto_migrate": true
          }
      }

2. **Migration Process**:

   .. code-block:: python

      def migrate_preferences(migration_data, api_token):
          url = 'http://example.com/api/v1/preferences/migrate/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=migration_data
          )
          
          return response.json()

Best Practices
------------

1. **Preference Design**:
   
   * Intuitive options
   * Sensible defaults
   * Clear categories
   * Easy navigation
   * Regular backups

2. **User Experience**:
   
   * Quick access
   * Live preview
   * Clear labels
   * Help text
   * Undo options

3. **Maintenance**:
   
   * Regular review
   * Clean unused
   * Update defaults
   * Monitor usage
   * Gather feedback

Troubleshooting
-------------

Common preference issues and solutions:

1. **Setting Issues**:
   
   * Check values
   * Verify format
   * Reset defaults
   * Clear cache
   * Update client

2. **Sync Issues**:
   
   * Check connection
   * Verify storage
   * Force refresh
   * Clear local data
   * Update version

3. **Migration Issues**:
   
   * Backup data
   * Check versions
   * Verify rules
   * Test changes
   * Monitor errors

Support
------

For preference issues:

1. Check the :doc:`troubleshooting` guide
2. Review preferences documentation
3. Contact support with:
   * User details
   * Preference data
   * Error messages
   * Version info 