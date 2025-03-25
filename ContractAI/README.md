# ContractAI

ContractAI is an AI-powered contract analysis platform that helps users extract, analyze, and understand legal documents.

## Project Structure

```
ContractAI/
├── app/                      # Main application package
│   ├── ai/                   # AI models and utilities
│   │   ├── models/           # Machine learning models
│   │   │   ├── bert/         # BERT-based models for clause extraction
│   │   │   ├── gpt/          # GPT-based models for text analysis
│   │   │   └── custom/       # Custom models
│   ├── api/                  # API endpoints
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── documents.py      # Document management endpoints
│   │   ├── analysis.py       # Analysis endpoints
│   │   └── admin.py          # Admin endpoints
│   ├── core/                 # Core functionality
│   │   ├── security.py       # Security utilities
│   │   ├── errors.py         # Error handling
│   │   └── utils.py          # Utility functions
│   ├── services/             # Business logic services
│   │   ├── document_service.py # Document processing service
│   │   └── storage_service.py  # Storage service (Minio)
│   ├── models/               # Database models
│   ├── config.py             # Application configuration
│   ├── database.py           # Database setup and models
│   └── main.py               # Application entry point
├── frontend/                 # Frontend web application
│   ├── css/                  # CSS styles
│   ├── js/                   # JavaScript files
│   ├── images/               # Image assets
│   ├── index.html            # Landing page
│   ├── login.html            # Login page
│   ├── signup.html           # Signup page
│   ├── dashboard.html        # User dashboard
│   ├── product.html          # Product page
│   └── pricing.html          # Pricing page
└── tests/                    # Test suite
```

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Minio (for document storage)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ContractAI.git
   cd ContractAI
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/contractai
   SECRET_KEY=your-secret-key-for-jwt-here-make-it-very-long-and-random
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   MINIO_SECURE=False
   REDIS_URL=redis://localhost:6379/0
   ```

5. Initialize the database:
   ```
   python -m app.main
   ```

## Running the Application

### Backend

```
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend

The frontend is static HTML/CSS/JS and can be served using any web server. For development, you can use Python's built-in HTTP server:

```
cd frontend
python -m http.server 3000
```

The frontend will be available at http://localhost:3000

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the tests with:

```
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.