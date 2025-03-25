@echo off
setlocal enabledelayedexpansion

REM Base directory - adjust this path as needed
set "BASE_DIR=ContractAI"

REM 1. Create missing frontend pages
echo Creating missing frontend pages...
set "FRONTEND_DIR=%BASE_DIR%\frontend"
for %%f in (
    "pricing.html"
    "dashboard.html"
    "signup.html"
    "login.html"
) do (
    if not exist "%FRONTEND_DIR%\%%f" (
        echo Creating %%f
        type nul > "%FRONTEND_DIR%\%%f"
    )
)

REM 2. Create AI models directory
echo Creating AI models directory...
set "AI_MODELS_DIR=%BASE_DIR%\app\ai\models"
if not exist "%AI_MODELS_DIR%" (
    mkdir "%AI_MODELS_DIR%"
    type nul > "%AI_MODELS_DIR%\__init__.py"
)

REM 3. Create shared resources directory
echo Creating shared resources structure...
set "SHARED_DIR=%BASE_DIR%\..\shared"
for %%d in (
    "branding"
    "components"
    "utils\ai-core"
) do (
    if not exist "%SHARED_DIR%\%%d" mkdir "%SHARED_DIR%\%%d"
)

REM 4. Create infrastructure directory
echo Creating infrastructure configuration...
set "INFRA_DIR=%BASE_DIR%\..\infrastructure"
for %%d in (
    "kubernetes"
    "terraform"
    "monitoring\grafana"
) do (
    if not exist "%INFRA_DIR%\%%d" mkdir "%INFRA_DIR%\%%d"
)

REM 5. Create future product placeholders
echo Creating future product directories...
for %%d in (
    "HR-DocAI"
    "SupplyDocAI"
    "ExpenseDocAI"
) do (
    if not exist "%BASE_DIR%\..\%%d" (
        mkdir "%BASE_DIR%\..\%%d"
        echo # %%d - Future DocMatrix AI Product > "%BASE_DIR%\..\%%d\README.md"
    )
)

echo Structure update completed successfully. 