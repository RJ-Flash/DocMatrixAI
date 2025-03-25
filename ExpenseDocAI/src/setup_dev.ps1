# Setup development environment for ExpenseDocAI
Write-Host "Setting up ExpenseDocAI development environment..."

# Create virtual environment
Write-Host "`nCreating virtual environment..."
if (-not (Test-Path "venv")) {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        exit 1
    }
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`nInstalling dependencies..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies"
    exit 1
}

# Install development dependencies
Write-Host "`nInstalling development dependencies..."
pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install development dependencies"
    exit 1
}

# Create necessary directories
Write-Host "`nCreating necessary directories..."
$directories = @(
    "logs",
    "media",
    "staticfiles",
    "media/expenses"
)
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

# Create .env file if it doesn't exist
Write-Host "`nCreating .env file..."
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Please update .env with your configuration"
}

# Initialize database
Write-Host "`nInitializing database..."
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to initialize database"
    exit 1
}

# Create superuser if it doesn't exist
Write-Host "`nChecking for superuser..."
$superuserCheck = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"
if ($superuserCheck -eq "False") {
    Write-Host "Creating superuser..."
    python manage.py createsuperuser
}

# Install pre-commit hooks
Write-Host "`nInstalling pre-commit hooks..."
pre-commit install
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install pre-commit hooks"
    exit 1
}

# Collect static files
Write-Host "`nCollecting static files..."
python manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to collect static files"
    exit 1
}

# Run tests
Write-Host "`nRunning tests..."
pytest
if ($LASTEXITCODE -ne 0) {
    Write-Error "Tests failed"
    exit 1
}

# Setup complete
Write-Host "`nDevelopment environment setup complete!" -ForegroundColor Green
Write-Host @"

Next steps:
1. Update .env with your configuration
2. Start the development server: python manage.py runserver
3. Access the admin interface at http://localhost:8000/admin/
4. Access the API at http://localhost:8000/api/v1/

For deployment:
1. Update deployment settings in settings.py
2. Run deploy.ps1 script

For monitoring:
1. Update monitoring settings in monitor.py
2. Run schedule_monitor.ps1 script
"@ 