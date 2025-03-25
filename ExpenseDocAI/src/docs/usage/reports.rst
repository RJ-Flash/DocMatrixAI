Reports and Analytics Guide
=======================

This guide explains how to use the reporting and analytics features in ExpenseDocAI.

Report Types
----------

ExpenseDocAI offers various report types:

1. **Expense Reports**
   ~~~~~~~~~~~~~~~

   Track expense metrics and trends:

   .. code-block:: json

      {
          "expense_report": {
              "type": "summary",
              "period": "monthly",
              "grouping": ["category", "department"],
              "metrics": [
                  "total_amount",
                  "average_amount",
                  "transaction_count",
                  "unique_vendors"
              ],
              "filters": {
                  "start_date": "2024-01-01",
                  "end_date": "2024-12-31",
                  "min_amount": 100.00,
                  "categories": ["travel", "meals"]
              }
          }
      }

2. **Compliance Reports**
   ~~~~~~~~~~~~~~~~~

   Monitor policy compliance:

   .. code-block:: json

      {
          "compliance_report": {
              "type": "violations",
              "period": "quarterly",
              "metrics": [
                  "violation_count",
                  "violation_amount",
                  "violation_rate",
                  "resolution_time"
              ],
              "categories": [
                  "amount_exceeded",
                  "policy_violation",
                  "missing_receipt",
                  "late_submission"
              ]
          }
      }

Report Generation
--------------

Generate reports through the API:

1. **Create Report**:

   .. code-block:: python

      def create_report(report_data, api_token):
          url = 'http://example.com/api/v1/reports/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=report_data
          )
          
          return response.json()

2. **Schedule Report**:

   .. code-block:: python

      def schedule_report(schedule_data, api_token):
          url = 'http://example.com/api/v1/reports/schedule/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'report_id': schedule_data['report_id'],
                  'frequency': schedule_data['frequency'],
                  'recipients': schedule_data['recipients'],
                  'format': schedule_data['format'],
                  'delivery_method': schedule_data['delivery_method']
              }
          )
          
          return response.json()

Analytics Features
---------------

1. **Trend Analysis**:
   
   * Expense patterns
   * Category trends
   * Vendor analysis
   * User behavior
   * Policy impact

2. **Predictive Analytics**:
   
   * Budget forecasting
   * Spend prediction
   * Anomaly detection
   * Risk assessment
   * Cost optimization

3. **Custom Analytics**:

   .. code-block:: python

      def create_custom_analytics(analytics_data, api_token):
          url = 'http://example.com/api/v1/analytics/custom/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'metrics': analytics_data['metrics'],
                  'dimensions': analytics_data['dimensions'],
                  'filters': analytics_data['filters'],
                  'calculations': analytics_data['calculations'],
                  'visualizations': analytics_data['visualizations']
              }
          )
          
          return response.json()

Dashboard Configuration
-------------------

Configure analytics dashboards:

1. **Dashboard Layout**:

   .. code-block:: json

      {
          "dashboard": {
              "name": "Expense Overview",
              "layout": "grid",
              "refresh_rate": 300,
              "widgets": [
                  {
                      "type": "chart",
                      "name": "Monthly Expenses",
                      "chart_type": "line",
                      "data_source": "expense_summary",
                      "position": {"row": 1, "col": 1}
                  },
                  {
                      "type": "metric",
                      "name": "Total Expenses",
                      "calculation": "sum",
                      "data_source": "expense_total",
                      "position": {"row": 1, "col": 2}
                  }
              ]
          }
      }

2. **Widget Configuration**:

   .. code-block:: python

      def configure_widget(widget_data, api_token):
          url = 'http://example.com/api/v1/dashboards/widgets/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=widget_data
          )
          
          return response.json()

Export Options
-----------

Export reports in various formats:

1. **Export Formats**:
   
   * PDF
   * Excel
   * CSV
   * JSON
   * HTML

2. **Export Configuration**:

   .. code-block:: python

      def export_report(export_data, api_token):
          url = 'http://example.com/api/v1/reports/export/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json={
                  'report_id': export_data['report_id'],
                  'format': export_data['format'],
                  'include_charts': export_data['include_charts'],
                  'password_protect': export_data['password_protect'],
                  'recipient_email': export_data['recipient_email']
              }
          )
          
          return response.json()

Best Practices
------------

1. **Report Design**:
   
   * Clear purpose
   * Relevant metrics
   * Clean layout
   * Easy navigation
   * Fast loading

2. **Data Quality**:
   
   * Regular validation
   * Clean data
   * Clear labels
   * Consistent formats
   * Accurate calculations

3. **Performance**:
   
   * Optimize queries
   * Cache results
   * Schedule updates
   * Limit data
   * Monitor usage

Troubleshooting
-------------

Common reporting issues and solutions:

1. **Data Issues**:
   
   * Verify sources
   * Check calculations
   * Update filters
   * Clean cache
   * Refresh data

2. **Performance Issues**:
   
   * Optimize queries
   * Reduce complexity
   * Update schedules
   * Clear cache
   * Monitor resources

3. **Export Issues**:
   
   * Check formats
   * Verify size
   * Test delivery
   * Update templates
   * Monitor errors

Support
------

For reporting issues:

1. Check the :doc:`troubleshooting` guide
2. Review analytics documentation
3. Contact support with:
   * Report details
   * Error messages
   * Sample data
   * Configuration info 