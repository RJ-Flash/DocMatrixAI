# Script to build ExpenseDocAI documentation
param(
    [switch]$Clean = $false,
    [switch]$Serve = $false,
    [int]$Port = 8000
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to check if a command exists
function Test-Command($Command) {
    try {
        Get-Command $Command -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# Function to create directory if it doesn't exist
function Ensure-Directory($Path) {
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

# Check if Python is installed
if (-not (Test-Command "python")) {
    Write-Error "Python is not installed. Please install Python and try again."
    exit 1
}

# Check if pip is installed
if (-not (Test-Command "pip")) {
    Write-Error "pip is not installed. Please install pip and try again."
    exit 1
}

# Create and activate virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
if ($IsWindows) {
    .\.venv\Scripts\Activate.ps1
}
else {
    . ./.venv/bin/Activate.ps1
}

# Install dependencies
Write-Host "Installing documentation dependencies..."
pip install -r requirements-dev.txt

# Create necessary directories
Ensure-Directory "docs/_static"
Ensure-Directory "docs/_templates"
Ensure-Directory "docs/_build"

# Clean build directory if requested
if ($Clean) {
    Write-Host "Cleaning build directory..."
    Remove-Item -Path "docs/_build/*" -Recurse -Force -ErrorAction SilentlyContinue
}

# Build documentation
Write-Host "Building documentation..."
Set-Location docs
sphinx-build -b html . _build/html

# Check for build errors
if ($LASTEXITCODE -ne 0) {
    Write-Error "Documentation build failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "Documentation built successfully!"
Write-Host "Output is in docs/_build/html/"

# Serve documentation if requested
if ($Serve) {
    Write-Host "Starting documentation server on http://localhost:$Port"
    python -m http.server $Port --directory _build/html
}

# Return to original directory
Set-Location .. 