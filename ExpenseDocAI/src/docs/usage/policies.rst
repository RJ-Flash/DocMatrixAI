Policy Configuration Guide
=======================

This guide explains how to configure and manage expense policies in ExpenseDocAI.

Policy Types
----------

ExpenseDocAI supports several types of expense policies:

1. **Amount Limits**
   ~~~~~~~~~~~~~~

   Set maximum amounts for different expense categories:

   .. code-block:: json

      {
          "amount_limits": {
              "meals": {
                  "max_amount": 100.00,
                  "currency": "USD",
                  "period": "daily"
              },
              "travel": {
                  "max_amount": 1000.00,
                  "currency": "USD",
                  "period": "per_expense"
              },
              "office_supplies": {
                  "max_amount": 500.00,
                  "currency": "USD",
                  "period": "monthly"
              }
          }
      }

2. **Category Rules**
   ~~~~~~~~~~~~~~~

   Define rules for specific expense categories:

   .. code-block:: json

      {
          "category_rules": {
              "travel": {
                  "requires_approval": true,
                  "approval_threshold": 500.00,
                  "allowed_vendors": ["Airlines", "Hotels", "Car Rental"],
                  "restricted_days": ["Saturday", "Sunday"]
              },
              "entertainment": {
                  "requires_justification": true,
                  "max_attendees": 10,
                  "restricted_vendors": ["Bars", "Clubs"]
              }
          }
      }

3. **Time Restrictions**
   ~~~~~~~~~~~~~~~~~

   Set time-based restrictions:

   .. code-block:: json

      {
          "time_restrictions": {
              "submission_deadline": {
                  "days": 30,
                  "from": "expense_date"
              },
              "blackout_periods": [
                  {
                      "start": "2024-12-20",
                      "end": "2024-12-31",
                      "reason": "Year-end closing"
                  }
              ],
              "weekend_policy": {
                  "allowed": false,
                  "exceptions": ["travel", "client_entertainment"]
              }
          }
      }

4. **Approval Rules**
   ~~~~~~~~~~~~~~~

   Configure approval workflows:

   .. code-block:: json

      {
          "approval_rules": {
              "thresholds": [
                  {
                      "amount": 100.00,
                      "approvers": ["manager"],
                      "auto_approve": true
                  },
                  {
                      "amount": 1000.00,
                      "approvers": ["manager", "department_head"],
                      "auto_approve": false
                  },
                  {
                      "amount": 5000.00,
                      "approvers": ["manager", "department_head", "finance"],
                      "auto_approve": false
                  }
              ],
              "special_categories": {
                  "travel": {
                      "approvers": ["travel_coordinator", "manager"],
                      "pre_approval_required": true
                  }
              }
          }
      }

Policy Configuration
-----------------

Configure policies through the API:

1. **Create Policy**:

   .. code-block:: python

      import requests
      
      def create_policy(policy_data, api_token):
          url = 'http://example.com/api/v1/policies/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=policy_data
          )
          
          return response.json()

2. **Update Policy**:

   .. code-block:: python

      def update_policy(policy_id, policy_data, api_token):
          url = f'http://example.com/api/v1/policies/{policy_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.put(
              url,
              headers=headers,
              json=policy_data
          )
          
          return response.json()

3. **Get Policy**:

   .. code-block:: python

      def get_policy(policy_id, api_token):
          url = f'http://example.com/api/v1/policies/{policy_id}/'
          headers = {'Authorization': f'Bearer {api_token}'}
          
          response = requests.get(
              url,
              headers=headers
          )
          
          return response.json()

Policy Validation
---------------

ExpenseDocAI validates expenses against configured policies:

1. **Amount Validation**:
   
   * Checks expense amounts against limits
   * Considers currency conversion
   * Tracks period-based limits

2. **Category Validation**:
   
   * Verifies allowed categories
   * Checks vendor restrictions
   * Validates required fields

3. **Time Validation**:
   
   * Checks submission deadlines
   * Validates expense dates
   * Enforces blackout periods

4. **Approval Validation**:
   
   * Determines required approvers
   * Checks pre-approval requirements
   * Validates approval workflow

Policy Violations
--------------

When a policy violation is detected:

1. **Violation Types**:
   
   * Amount exceeded
   * Invalid category
   * Late submission
   * Missing approval
   * Restricted vendor

2. **Violation Response**:
   
   * Record violation details
   * Notify relevant parties
   * Block or flag for review
   * Request justification

3. **Violation Handling**:

   .. code-block:: python

      def handle_violation(violation_data, api_token):
          url = 'http://example.com/api/v1/violations/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'expense_id': violation_data['expense_id'],
                  'policy_id': violation_data['policy_id'],
                  'violation_type': violation_data['type'],
                  'details': violation_data['details'],
                  'resolution': violation_data['resolution']
              }
          )
          
          return response.json()

Best Practices
------------

1. **Policy Design**:
   
   * Keep policies simple and clear
   * Use consistent rules
   * Document exceptions
   * Regular policy review
   * Test before deployment

2. **Implementation**:
   
   * Start with basic rules
   * Gradually add complexity
   * Monitor effectiveness
   * Gather user feedback
   * Regular updates

3. **Communication**:
   
   * Clear policy documentation
   * Regular training sessions
   * Update notifications
   * Feedback channels
   * Support resources

4. **Maintenance**:
   
   * Regular policy review
   * Update as needed
   * Monitor compliance
   * Track exceptions
   * Audit policy changes

Troubleshooting
-------------

Common policy issues and solutions:

1. **Policy Conflicts**:
   
   * Review rule hierarchy
   * Check for overlaps
   * Resolve contradictions
   * Document exceptions
   * Test changes

2. **Performance Issues**:
   
   * Optimize rule complexity
   * Cache policy data
   * Monitor validation time
   * Scale resources
   * Regular cleanup

3. **User Issues**:
   
   * Improve documentation
   * Provide training
   * Clear error messages
   * Support channels
   * Regular feedback

Support
------

For policy-related issues:

1. Check the :doc:`troubleshooting` guide
2. Review policy documentation
3. Contact support with:
   * Policy details
   * Violation examples
   * Error messages
   * Configuration data 