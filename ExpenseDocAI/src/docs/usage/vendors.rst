Vendor Management Guide
====================

This guide explains how to manage vendors and merchants in ExpenseDocAI.

Vendor Structure
-------------

ExpenseDocAI organizes vendors in a structured way:

1. **Vendor Categories**
   ~~~~~~~~~~~~~~~~

   Top-level vendor classifications:

   .. code-block:: json

      {
          "vendor_categories": [
              "airlines",
              "hotels",
              "restaurants",
              "office_supplies",
              "technology",
              "transportation",
              "professional_services",
              "utilities"
          ]
      }

2. **Vendor Profiles**
   ~~~~~~~~~~~~~~~

   Detailed vendor information:

   .. code-block:: json

      {
          "vendor": {
              "name": "Delta Airlines",
              "category": "airlines",
              "tax_id": "123456789",
              "preferred": true,
              "contract_number": "DA2024001",
              "payment_terms": "net30",
              "currency": "USD",
              "contact": {
                  "email": "corporate@delta.com",
                  "phone": "+1-800-123-4567",
                  "website": "https://www.delta.com"
              }
          }
      }

Vendor Configuration
-----------------

Configure vendors through the API:

1. **Create Vendor**:

   .. code-block:: python

      def create_vendor(vendor_data, api_token):
          url = 'http://example.com/api/v1/vendors/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=vendor_data
          )
          
          return response.json()

2. **Update Vendor**:

   .. code-block:: python

      def update_vendor(vendor_id, vendor_data, api_token):
          url = f'http://example.com/api/v1/vendors/{vendor_id}/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.put(
              url,
              headers=headers,
              json=vendor_data
          )
          
          return response.json()

Vendor Validation
--------------

ExpenseDocAI validates vendors during expense processing:

1. **Basic Validation**:
   
   * Vendor existence
   * Category match
   * Active status
   * Tax ID format
   * Currency support

2. **Policy Validation**:
   
   * Preferred vendor status
   * Spending limits
   * Category restrictions
   * Payment terms
   * Contract compliance

3. **Data Enrichment**:
   
   * Auto-categorization
   * Tax information
   * Location data
   * Contact details
   * Payment methods

Vendor Management
--------------

1. **Bulk Operations**:

   .. code-block:: python

      def bulk_update_vendors(vendors_data, api_token):
          url = 'http://example.com/api/v1/vendors/bulk/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=vendors_data
          )
          
          return response.json()

2. **Vendor Import/Export**:

   .. code-block:: python

      def export_vendors(api_token):
          url = 'http://example.com/api/v1/vendors/export/'
          headers = {'Authorization': f'Bearer {api_token}'}
          
          response = requests.get(
              url,
              headers=headers
          )
          
          return response.json()

Vendor Analytics
-------------

Generate vendor-related analytics:

1. **Spend Analysis**:
   
   * Total spend
   * Category breakdown
   * Trend analysis
   * Payment patterns
   * Compliance rates

2. **Performance Metrics**:
   
   * Processing time
   * Error rates
   * Match accuracy
   * Policy compliance
   * User satisfaction

3. **Report Generation**:

   .. code-block:: python

      def generate_vendor_report(report_params, api_token):
          url = 'http://example.com/api/v1/reports/vendors/'
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

Vendor Matching
------------

ExpenseDocAI uses advanced matching for vendors:

1. **Match Methods**:
   
   * Exact name match
   * Fuzzy matching
   * Address matching
   * Tax ID matching
   * Phone/email matching

2. **Match Rules**:

   .. code-block:: json

      {
          "matching_rules": {
              "exact_match": {
                  "fields": ["tax_id", "contract_number"],
                  "score": 100
              },
              "fuzzy_match": {
                  "fields": ["name", "address"],
                  "min_score": 85
              },
              "partial_match": {
                  "fields": ["phone", "email"],
                  "min_score": 70
              }
          }
      }

3. **Match Processing**:

   .. code-block:: python

      def process_vendor_match(vendor_data, api_token):
          url = 'http://example.com/api/v1/vendors/match/'
          headers = {
              'Authorization': f'Bearer {api_token}',
              'Content-Type': 'application/json'
          }
          
          response = requests.post(
              url,
              headers=headers,
              json=vendor_data
          )
          
          return response.json()

Best Practices
------------

1. **Vendor Setup**:
   
   * Verify information
   * Complete profiles
   * Regular updates
   * Clear categories
   * Document rules

2. **Data Quality**:
   
   * Standardize names
   * Validate tax IDs
   * Update contacts
   * Check duplicates
   * Clean addresses

3. **Maintenance**:
   
   * Regular review
   * Update rules
   * Monitor matches
   * Clean database
   * Audit changes

Troubleshooting
-------------

Common vendor issues and solutions:

1. **Match Issues**:
   
   * Check rules
   * Verify data
   * Update profiles
   * Test matching
   * Monitor results

2. **Data Problems**:
   
   * Clean entries
   * Fix formats
   * Update missing
   * Remove duplicates
   * Verify sources

3. **Integration Issues**:
   
   * Check APIs
   * Test sync
   * Monitor errors
   * Update mappings
   * Verify formats

Support
------

For vendor-related issues:

1. Check the :doc:`troubleshooting` guide
2. Review vendor documentation
3. Contact support with:
   * Vendor details
   * Match examples
   * Error messages
   * Configuration data 