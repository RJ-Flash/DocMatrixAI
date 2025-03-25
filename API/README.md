# DocMatrix AI API Server

This is the backend API server for DocMatrix AI, providing document processing and analysis capabilities.

## Features

- User Authentication (register, login, password reset)
- Document Upload and Management
- Document Processing:
  - Contract Analysis
  - Expense Document Processing
  - HR Document Management
  - Supply Chain Document Analysis
- Secure File Storage (AWS S3)
- Document Text Extraction (AWS Textract)
- AI-Powered Analysis (OpenAI GPT)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create .env file:
```bash
cp .env.example .env
```

3. Configure environment variables in .env:
- MongoDB connection
- AWS credentials
- OpenAI API key
- SMTP settings
- JWT secrets

4. Start the server:
```bash
# Development
npm run dev

# Production
npm start
```

## API Endpoints

### Authentication
- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - Login user
- GET /api/v1/auth/logout - Logout user
- GET /api/v1/auth/me - Get current user
- POST /api/v1/auth/forgotpassword - Request password reset
- PUT /api/v1/auth/resetpassword/:resettoken - Reset password
- GET /api/v1/auth/verify-email/:token - Verify email

### Documents
- POST /api/v1/documents - Upload document
- GET /api/v1/documents - Get all documents
- GET /api/v1/documents/:id - Get single document
- DELETE /api/v1/documents/:id - Delete document
- POST /api/v1/documents/:id/process - Process document

## Security

- JWT Authentication
- Rate Limiting
- CORS Protection
- XSS Prevention
- Security Headers (helmet)
- Parameter Pollution Prevention
- File Upload Restrictions

## Error Handling

The API uses a centralized error handling system with proper error messages and status codes.

## Logging

Winston logger is configured for:
- Error logging
- API request logging
- System events

## Contributing

1. Create feature branch
2. Commit changes
3. Create pull request

## License

Proprietary - DocMatrix AI
