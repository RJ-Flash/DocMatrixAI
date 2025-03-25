# Script to validate API documentation and run tests

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to check if a command exists
function Test-Command($command) {
    try { Get-Command $command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to create virtual environment
function Create-VirtualEnv {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    if (Test-Command "python") {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
    } else {
        throw "Python not found in PATH"
    }
}

# Function to activate virtual environment
function Activate-VirtualEnv {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    if (Test-Path ".venv/Scripts/Activate.ps1") {
        & .venv/Scripts/Activate.ps1
    } else {
        throw "Virtual environment activation script not found"
    }
}

# Function to install dependencies
function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
    pip install pytest pytest-cov requests
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install dependencies"
    }
}

# Function to run API tests
function Run-ApiTests {
    param (
        [string]$Category = "all"
    )
    Write-Host "Running API tests..." -ForegroundColor Green
    
    $testCommand = "pytest tests/test_api_examples.py -v --cov=tests --cov-report=html --cov-report=xml"
    
    switch ($Category) {
        "auth" { $testCommand += " -m auth" }
        "upload" { $testCommand += " -m upload" }
        "processing" { $testCommand += " -m processing" }
        "sdk" { $testCommand += " -m sdk" }
        "docs" { $testCommand += " -m docs" }
        "api" { $testCommand += " -m api" }
    }
    
    Invoke-Expression $testCommand
    if ($LASTEXITCODE -ne 0) {
        throw "API tests failed"
    }
}

# Function to build documentation
function Build-Documentation {
    Write-Host "Building documentation..." -ForegroundColor Green
    sphinx-build -b html . _build/html
    if ($LASTEXITCODE -ne 0) {
        throw "Documentation build failed"
    }
}

# Function to check links
function Check-Links {
    Write-Host "Checking documentation links..." -ForegroundColor Green
    sphinx-build -b linkcheck . _build/linkcheck
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Some links are broken. Check _build/linkcheck/output.txt for details"
    }
}

# Function to run doctests
function Run-Doctests {
    Write-Host "Running doctests..." -ForegroundColor Green
    sphinx-build -b doctest . _build/doctest
    if ($LASTEXITCODE -ne 0) {
        throw "Doctests failed"
    }
}

# Function to display test categories
function Show-TestCategories {
    Write-Host "Available test categories:" -ForegroundColor Green
    Write-Host "  all        - Run all tests"
    Write-Host "  auth       - Authentication tests"
    Write-Host "  upload     - Document upload tests"
    Write-Host "  processing - Document processing tests"
    Write-Host "  sdk        - SDK integration tests"
    Write-Host "  docs       - Documentation examples"
    Write-Host "  api        - All API endpoint tests"
}

# Main execution block
try {
    # Parse command line arguments
    param (
        [Parameter(Position=0)]
        [string]$Category = "all",
        
        [Parameter()]
        [switch]$Help,
        
        [Parameter()]
        [switch]$SkipDocs,
        
        [Parameter()]
        [switch]$SkipTests
    )

    if ($Help) {
        Show-TestCategories
        exit 0
    }

    # Create and activate virtual environment if it doesn't exist
    if (-not (Test-Path ".venv")) {
        Create-VirtualEnv
    }
    Activate-VirtualEnv

    # Install dependencies
    Install-Dependencies

    # Run API tests if not skipped
    if (-not $SkipTests) {
        Run-ApiTests -Category $Category
    }

    # Build and validate documentation if not skipped
    if (-not $SkipDocs) {
        Build-Documentation
        Check-Links
        Run-Doctests
    }

    # Open coverage report
    if ((-not $SkipTests) -and (Test-Path "coverage_html/index.html")) {
        Start-Process "coverage_html/index.html"
    }

    # Open documentation
    if ((-not $SkipDocs) -and (Test-Path "_build/html/index.html")) {
        Start-Process "_build/html/index.html"
    }

    Write-Host "Validation completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
} 