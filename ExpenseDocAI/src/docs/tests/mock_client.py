"""Mock client for ExpenseDocAI testing."""

class MockDocument:
    """Mock document object."""
    def __init__(self, id, status):
        self.id = id
        self.status = status

class MockDocuments:
    """Mock documents API."""
    def create(self, file):
        """Create a document."""
        return MockDocument("test-doc-123", "pending")
    
    def get(self, doc_id):
        """Get a document."""
        return MockDocument(doc_id, "processing")

class MockEntry:
    """Mock entry object."""
    def __init__(self, id, amount, date, vendor, category):
        self.id = id
        self.amount = amount
        self.date = date
        self.vendor = vendor
        self.category = category

class MockEntries:
    """Mock entries API."""
    def list(self, start_date=None, end_date=None):
        """List entries."""
        return MockEntriesResponse([
            MockEntry("test-entry-123", 100.00, "2024-01-15", "Test Vendor", "travel")
        ])

class MockEntriesResponse:
    """Mock entries response."""
    def __init__(self, entries):
        self.data = entries

class Client:
    """Mock ExpenseDocAI client."""
    def __init__(self, api_key=None):
        self.documents = MockDocuments()
        self.entries = MockEntries() 