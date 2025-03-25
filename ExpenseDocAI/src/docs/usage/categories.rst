Expense Categories Guide
=====================

This guide explains how to manage and configure expense categories in ExpenseDocAI.

Category Structure
---------------

ExpenseDocAI uses a hierarchical category structure:

1. **Main Categories**
   ~~~~~~~~~~~~~~~

   Top-level expense classifications:

   .. code-block:: json

      {
          "main_categories": [
              "travel",
              "meals",
              "office",
              "equipment",
              "services",
              "entertainment",
              "utilities",
              "training"
          ]
      }

2. **Subcategories**
   ~~~~~~~~~~~~~

   Detailed classifications under main categories:

   .. code-block:: json

      {
          "travel": {
              "subcategories": [
                  "airfare",
                  "hotel",
                  "car_rental",
                  "taxi",
                  "parking",
                  "train",
                  "mileage"
              ]
          },
          "meals": {
              "subcategories": [
                  "business_meals",
                  "team_lunch",
                  "client_dinner",
                  "conference_meals"
              ]
          }
      }

Category Configuration
-------------------

Configure categories through the API:

1. **Create Category**:

   .. code-block:: python

      def create_category(category_data, api_token):
          url = 'http://example.com/api/v1/categories/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=category_data
          )
          
          return response.json()

2. **Update Category**:

   .. code-block:: python

      def update_category(category_id, category_data, api_token):
          url = f'http://example.com/api/v1/categories/{category_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.put(
              url,
              headers=headers,
              json=category_data
          )
          
          return response.json()

Category Attributes
----------------

Each category can have specific attributes:

1. **Basic Attributes**:
   
   .. code-block:: json

      {
          "category": {
              "name": "travel",
              "code": "TRV",
              "description": "Travel-related expenses",
              "active": true,
              "tax_deductible": true,
              "gl_account": "6200",
              "department_restricted": false
          }
      }

2. **Validation Rules**:
   
   .. code-block:: json

      {
          "validation_rules": {
              "required_fields": [
                  "date",
                  "amount",
                  "vendor",
                  "receipt"
              ],
              "optional_fields": [
                  "description",
                  "attendees",
                  "project_code"
              ],
              "custom_fields": [
                  {
                      "name": "trip_purpose",
                      "type": "text",
                      "required": true
                  }
              ]
          }
      }

Category Management
----------------

1. **Bulk Operations**:

   .. code-block:: python

      def bulk_update_categories(categories_data, api_token):
          url = 'http://example.com/api/v1/categories/bulk/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=categories_data
          )
          
          return response.json()

2. **Category Import/Export**:

   .. code-block:: python

      def export_categories(api_token):
          url = 'http://example.com/api/v1/categories/export/'
          headers = {'Authorization': f'Bearer {api_token}'}
          
          response = requests.get(
              url,
              headers=headers
          )
          
          return response.json()

Category Reporting
---------------

Generate reports on category usage:

1. **Usage Statistics**:
   
   * Expense frequency
   * Total amounts
   * Average amounts
   * Trend analysis
   * Department breakdown

2. **Compliance Reports**:
   
   * Policy violations
   * Missing fields
   * Approval rates
   * Processing time
   * Exception tracking

3. **Report Generation**:

   .. code-block:: python

      def generate_category_report(report_params, api_token):
          url = 'http://example.com/api/v1/reports/categories/'
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

1. **Category Design**:
   
   * Use clear names
   * Logical hierarchy
   * Consistent coding
   * Regular review
   * User feedback

2. **Implementation**:
   
   * Start simple
   * Add detail gradually
   * Test thoroughly
   * Document changes
   * Train users

3. **Maintenance**:
   
   * Regular cleanup
   * Update mappings
   * Monitor usage
   * Gather feedback
   * Optimize structure

Troubleshooting
-------------

Common category issues and solutions:

1. **Mapping Issues**:
   
   * Check hierarchy
   * Verify codes
   * Update mappings
   * Fix duplicates
   * Test changes

2. **Integration Problems**:
   
   * Check APIs
   * Verify formats
   * Test sync
   * Log errors
   * Monitor performance

3. **User Problems**:
   
   * Improve UI
   * Clear guidance
   * Quick support
   * Regular training
   * Update docs

Support
------

For category-related issues:

1. Check the :doc:`troubleshooting` guide
2. Review category documentation
3. Contact support with:
   * Category details
   * Error messages
   * Example cases
   * Configuration data 