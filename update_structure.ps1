# Base directory - adjust this path as needed
$BASE_DIR = "ContractAI"

# 1. Create missing frontend pages
Write-Host "Creating missing frontend pages..."
$FRONTEND_DIR = Join-Path $BASE_DIR "frontend"
@(
    "pricing.html",
    "dashboard.html",
    "signup.html",
    "login.html"
) | ForEach-Object {
    $filePath = Join-Path $FRONTEND_DIR $_
    if (-not (Test-Path $filePath)) {
        Write-Host "Creating $_"
        New-Item -ItemType File -Path $filePath -Force | Out-Null
    }
}

# 2. Create AI models directory
Write-Host "Creating AI models directory..."
$AI_MODELS_DIR = Join-Path $BASE_DIR "app\ai\models"
if (-not (Test-Path $AI_MODELS_DIR)) {
    New-Item -ItemType Directory -Path $AI_MODELS_DIR -Force | Out-Null
    New-Item -ItemType File -Path (Join-Path $AI_MODELS_DIR "__init__.py") -Force | Out-Null
}

# 3. Create shared resources directory
Write-Host "Creating shared resources structure..."
$SHARED_DIR = Join-Path ".." "shared"
@(
    "branding",
    "components",
    "utils\ai-core"
) | ForEach-Object {
    $dirPath = Join-Path $SHARED_DIR $_
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
}

# 4. Create infrastructure directory
Write-Host "Creating infrastructure configuration..."
$INFRA_DIR = Join-Path ".." "infrastructure"
@(
    "kubernetes",
    "terraform",
    "monitoring\grafana"
) | ForEach-Object {
    $dirPath = Join-Path $INFRA_DIR $_
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
}

# 5. Create future product placeholders
Write-Host "Creating future product directories..."
@(
    "HR-DocAI",
    "SupplyDocAI",
    "ExpenseDocAI"
) | ForEach-Object {
    $dirPath = Join-Path ".." $_
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
        Set-Content -Path (Join-Path $dirPath "README.md") -Value "# $_ - Future DocMatrix AI Product"
    }
}

Write-Host "Structure update completed successfully." 