Approval Workflow Guide
===================

This guide explains how to manage approval workflows in ExpenseDocAI.

Workflow Structure
---------------

ExpenseDocAI supports flexible approval workflows:

1. **Approval Levels**
   ~~~~~~~~~~~~~~~

   Define hierarchical approval levels:

   .. code-block:: json

      {
          "approval_levels": [
              {
                  "level": 1,
                  "name": "manager",
                  "description": "Direct manager approval",
                  "required": true
              },
              {
                  "level": 2,
                  "name": "department_head",
                  "description": "Department head approval",
                  "threshold": 1000.00
              },
              {
                  "level": 3,
                  "name": "finance",
                  "description": "Finance team approval",
                  "threshold": 5000.00
              }
          ]
      }

2. **Approval Rules**
   ~~~~~~~~~~~~~~

   Configure approval routing rules:

   .. code-block:: json

      {
          "approval_rules": {
              "amount_based": {
                  "thresholds": [
                      {
                          "amount": 100.00,
                          "approvers": ["manager"],
                          "auto_approve": true
                      },
                      {
                          "amount": 1000.00,
                          "approvers": ["manager", "department_head"]
                      },
                      {
                          "amount": 5000.00,
                          "approvers": ["manager", "department_head", "finance"]
                      }
                  ]
              },
              "category_based": {
                  "travel": {
                      "approvers": ["travel_coordinator", "manager"],
                      "pre_approval": true
                  },
                  "equipment": {
                      "approvers": ["it_manager", "finance"],
                      "pre_approval": true
                  }
              }
          }
      }

Workflow Configuration
-------------------

Configure workflows through the API:

1. **Create Workflow**:

   .. code-block:: python

      def create_workflow(workflow_data, api_token):
          url = 'http://example.com/api/v1/workflows/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=workflow_data
          )
          
          return response.json()

2. **Update Workflow**:

   .. code-block:: python

      def update_workflow(workflow_id, workflow_data, api_token):
          url = f'http://example.com/api/v1/workflows/{workflow_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.put(
              url,
              headers=headers,
              json=workflow_data
          )
          
          return response.json()

Approval Process
-------------

ExpenseDocAI manages the approval lifecycle:

1. **Submission**:
   
   * Document validation
   * Policy checks
   * Route determination
   * Notification dispatch
   * Status tracking

2. **Review Process**:
   
   * Approver assignment
   * Document access
   * Comment capability
   * Action recording
   * Status updates

3. **Actions**:

   .. code-block:: python

      def process_approval(approval_data, api_token):
          url = 'http://example.com/api/v1/approvals/process/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'document_id': approval_data['document_id'],
                  'approver_id': approval_data['approver_id'],
                  'action': approval_data['action'],
                  'comments': approval_data['comments'],
                  'attachments': approval_data['attachments']
              }
          )
          
          return response.json()

Delegation Management
-----------------

Handle approval delegations:

1. **Delegate Setup**:

   .. code-block:: python

      def setup_delegation(delegation_data, api_token):
          url = 'http://example.com/api/v1/delegations/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'delegator_id': delegation_data['delegator_id'],
                  'delegate_id': delegation_data['delegate_id'],
                  'start_date': delegation_data['start_date'],
                  'end_date': delegation_data['end_date'],
                  'approval_types': delegation_data['approval_types']
              }
          )
          
          return response.json()

2. **Delegation Rules**:

   .. code-block:: json

      {
          "delegation_rules": {
              "max_duration": 30,
              "allowed_levels": ["manager", "department_head"],
              "restrictions": {
                  "amount_limit": 5000.00,
                  "categories": ["travel", "office_supplies"],
                  "exclude_categories": ["equipment"]
              }
          }
      }

Notification System
----------------

Configure approval notifications:

1. **Notification Types**:
   
   * New request
   * Reminder
   * Escalation
   * Approval
   * Rejection
   * Delegation

2. **Notification Config**:

   .. code-block:: json

      {
          "notifications": {
              "channels": {
                  "email": true,
                  "slack": true,
                  "mobile": true
              },
              "reminders": {
                  "frequency": "daily",
                  "max_reminders": 3
              },
              "escalation": {
                  "trigger_days": 5,
                  "notify_manager": true
              }
          }
      }

Reporting & Analytics
-----------------

Track approval metrics:

1. **Performance Metrics**:
   
   * Processing time
   * Approval rates
   * Bottlenecks
   * User activity
   * Exception rates

2. **Report Generation**:

   .. code-block:: python

      def generate_approval_report(report_params, api_token):
          url = 'http://example.com/api/v1/reports/approvals/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=report_params
          )
          
          return response.json()

Best Practices
------------

1. **Workflow Design**:
   
   * Clear hierarchy
   * Simple rules
   * Fast processing
   * Good coverage
   * Easy delegation

2. **Implementation**:
   
   * Test thoroughly
   * Monitor performance
   * Regular updates
   * User training
   * Clear documentation

3. **Maintenance**:
   
   * Review rules
   * Update flows
   * Clean queues
   * Check delegates
   * Audit trails

Troubleshooting
-------------

Common approval issues and solutions:

1. **Routing Issues**:
   
   * Check rules
   * Verify roles
   * Update hierarchy
   * Test flows
   * Monitor queues

2. **Performance Issues**:
   
   * Optimize rules
   * Clear backlogs
   * Update delegations
   * Monitor timing
   * Check bottlenecks

3. **User Issues**:
   
   * Verify access
   * Check notifications
   * Update training
   * Monitor feedback
   * Support response

Support
------

For approval-related issues:

1. Check the :doc:`troubleshooting` guide
2. Review workflow documentation
3. Contact support with:
   * Workflow details
   * Error messages
   * Example cases
   * Configuration data 