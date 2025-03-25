# DocMatrix AI Project Directory Structure Creation Script
Write-Host "Creating DocMatrix AI project directory structure..." -ForegroundColor Green

# Set the base directory to the current workspace
$BASE_DIR = Get-Location

Write-Host "Current directory: $BASE_DIR" -ForegroundColor Cyan

# Create frontend missing files (already exist, but ensuring structure is complete)
Write-Host "Creating Frontend files..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\frontend\css" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\frontend\js" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\frontend\images" -Force | Out-Null

# Create AI Models directory
Write-Host "Creating AI Models directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\app\ai\models" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\app\ai\models\bert" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\app\ai\models\gpt" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\app\ai\models\custom" -Force | Out-Null

# Create model initialization files if they don't exist
if (-not (Test-Path "$BASE_DIR\ContractAI\app\ai\models\__init__.py")) {
    @"
"""
AI models package for ContractAI.
This package contains the machine learning models used for contract analysis.
"""
"@ | Set-Content -Path "$BASE_DIR\ContractAI\app\ai\models\__init__.py"
}

if (-not (Test-Path "$BASE_DIR\ContractAI\app\ai\models\bert\__init__.py")) {
    @"
"""
BERT-based models for contract analysis.
"""
"@ | Set-Content -Path "$BASE_DIR\ContractAI\app\ai\models\bert\__init__.py"
}

if (-not (Test-Path "$BASE_DIR\ContractAI\app\ai\models\gpt\__init__.py")) {
    @"
"""
GPT-based models for contract analysis.
"""
"@ | Set-Content -Path "$BASE_DIR\ContractAI\app\ai\models\gpt\__init__.py"
}

if (-not (Test-Path "$BASE_DIR\ContractAI\app\ai\models\custom\__init__.py")) {
    @"
"""
Custom models for contract analysis.
"""
"@ | Set-Content -Path "$BASE_DIR\ContractAI\app\ai\models\custom\__init__.py"
}

# Create model implementation files
if (-not (Test-Path "$BASE_DIR\ContractAI\app\ai\models\bert\clause_extractor.py")) {
    @"
from transformers import BertTokenizer, BertForSequenceClassification
import torch

class BertClauseExtractor:
    def __init__(self, model_path='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        
    def extract_clauses(self, text):
        # Implementation for clause extraction using BERT
        pass
"@ | Set-Content -Path "$BASE_DIR\ContractAI\app\ai\models\bert\clause_extractor.py"
}

if (-not (Test-Path "$BASE_DIR\ContractAI\app\ai\models\gpt\text_analyzer.py")) {
    @"
import openai

class GPTTextAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
        
    def analyze_text(self, text, prompt=None):
        # Implementation for text analysis using GPT
        pass
"@ | Set-Content -Path "$BASE_DIR\ContractAI\app\ai\models\gpt\text_analyzer.py"
}

# Create Shared Resources
Write-Host "Creating Shared Resources..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$BASE_DIR\shared\branding\logos" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\shared\branding\themes" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\shared\components\ui" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\shared\components\widgets" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\shared\utils\ai-core" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\shared\utils\common" -Force | Out-Null

# Create shared component files
if (-not (Test-Path "$BASE_DIR\shared\components\ui\header.js")) {
    @"
// Shared header component for DocMatrix AI products
class Header {
    constructor(options = {}) {
        this.title = options.title || 'DocMatrix AI';
        this.logo = options.logo || '/shared/branding/logos/default.svg';
    }
    
    render() {
        // Implementation for rendering header
        return `<header class="docmatrix-header">
            <img src="\${this.logo}" alt="\${this.title} Logo" />
            <h1>\${this.title}</h1>
        </header>`;
    }
}

export default Header;
"@ | Set-Content -Path "$BASE_DIR\shared\components\ui\header.js"
}

if (-not (Test-Path "$BASE_DIR\shared\components\ui\footer.js")) {
    @"
// Shared footer component for DocMatrix AI products
class Footer {
    constructor(options = {}) {
        this.copyright = options.copyright || `© \${new Date().getFullYear()} DocMatrix AI`;
        this.links = options.links || [];
    }
    
    render() {
        // Implementation for rendering footer
        return `<footer class="docmatrix-footer">
            <p>\${this.copyright}</p>
        </footer>`;
    }
}

export default Footer;
"@ | Set-Content -Path "$BASE_DIR\shared\components\ui\footer.js"
}

# Create Infrastructure
Write-Host "Creating Infrastructure directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\kubernetes\deployments" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\kubernetes\services" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\kubernetes\configmaps" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\terraform\modules" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\terraform\environments" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\terraform\variables" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\monitoring\grafana" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\monitoring\prometheus" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\infrastructure\monitoring\alerts" -Force | Out-Null

# Create Kubernetes deployment files
if (-not (Test-Path "$BASE_DIR\infrastructure\kubernetes\deployments\contractai.yaml")) {
    @"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contractai
  labels:
    app: contractai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: contractai
  template:
    metadata:
      labels:
        app: contractai
    spec:
      containers:
      - name: contractai
        image: docmatrixai/contractai:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: contractai-secrets
              key: database-url
"@ | Set-Content -Path "$BASE_DIR\infrastructure\kubernetes\deployments\contractai.yaml"
}

if (-not (Test-Path "$BASE_DIR\infrastructure\kubernetes\services\contractai.yaml")) {
    @"
apiVersion: v1
kind: Service
metadata:
  name: contractai
spec:
  selector:
    app: contractai
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
"@ | Set-Content -Path "$BASE_DIR\infrastructure\kubernetes\services\contractai.yaml"
}

# Create Terraform files
if (-not (Test-Path "$BASE_DIR\infrastructure\terraform\main.tf")) {
    @"
provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
  # VPC configuration
}

module "eks" {
  source = "./modules/eks"
  # EKS configuration
}

module "rds" {
  source = "./modules/rds"
  # RDS configuration
}
"@ | Set-Content -Path "$BASE_DIR\infrastructure\terraform\main.tf"
}

# Create Future Product Placeholders
Write-Host "Creating Future Product Placeholders..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$BASE_DIR\HR-DocAI\docs" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\HR-DocAI\src" -Force | Out-Null
if (-not (Test-Path "$BASE_DIR\HR-DocAI\README.md")) {
    @"
# HR Document Compliance Management

HR-DocAI is an AI-powered solution for managing HR documents and ensuring compliance with regulations.

## Features

- Automated document classification
- Compliance checking against regulations
- Employee data extraction and validation
"@ | Set-Content -Path "$BASE_DIR\HR-DocAI\README.md"
}

New-Item -ItemType Directory -Path "$BASE_DIR\SupplyDocAI\docs" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\SupplyDocAI\src" -Force | Out-Null
if (-not (Test-Path "$BASE_DIR\SupplyDocAI\README.md")) {
    @"
# Supply Chain Documentation Automation

SupplyDocAI streamlines supply chain documentation processes using AI to extract, validate, and manage critical information.

## Features

- Purchase order analysis
- Shipping document verification
- Inventory reconciliation
"@ | Set-Content -Path "$BASE_DIR\SupplyDocAI\README.md"
}

New-Item -ItemType Directory -Path "$BASE_DIR\ExpenseDocAI\docs" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ExpenseDocAI\src" -Force | Out-Null
if (-not (Test-Path "$BASE_DIR\ExpenseDocAI\README.md")) {
    @"
# Expense Report Automation

ExpenseDocAI automates the processing of expense reports, receipts, and invoices using advanced AI techniques.

## Features

- Receipt OCR and data extraction
- Expense categorization
- Policy compliance checking
"@ | Set-Content -Path "$BASE_DIR\ExpenseDocAI\README.md"
}

# Create Configuration Files
Write-Host "Creating Configuration Files..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\config" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\scripts\setup" -Force | Out-Null
New-Item -ItemType Directory -Path "$BASE_DIR\ContractAI\scripts\deployment" -Force | Out-Null

if (-not (Test-Path "$BASE_DIR\ContractAI\config\development.yaml")) {
    @"
# Development Configuration
environment: development

database:
  host: localhost
  port: 5432
  name: contractai_dev
  user: dev_user
  
api:
  host: 0.0.0.0
  port: 8000
  debug: true
  
ai:
  models_path: ./app/ai/models
  openai_api_key: ${OPENAI_API_KEY}
"@ | Set-Content -Path "$BASE_DIR\ContractAI\config\development.yaml"
}

if (-not (Test-Path "$BASE_DIR\ContractAI\config\production.yaml")) {
    @"
# Production Configuration
environment: production

database:
  host: ${DB_HOST}
  port: 5432
  name: contractai_prod
  user: ${DB_USER}
  
api:
  host: 0.0.0.0
  port: 8000
  debug: false
  
ai:
  models_path: /opt/contractai/models
  openai_api_key: ${OPENAI_API_KEY}
"@ | Set-Content -Path "$BASE_DIR\ContractAI\config\production.yaml"
}

if (-not (Test-Path "$BASE_DIR\ContractAI\config\staging.yaml")) {
    @"
# Staging Configuration
environment: staging

database:
  host: ${DB_HOST}
  port: 5432
  name: contractai_staging
  user: ${DB_USER}
  
api:
  host: 0.0.0.0
  port: 8000
  debug: true
  
ai:
  models_path: /opt/contractai/models
  openai_api_key: ${OPENAI_API_KEY}
"@ | Set-Content -Path "$BASE_DIR\ContractAI\config\staging.yaml"
}

# Create CSS file for frontend
if (-not (Test-Path "$BASE_DIR\ContractAI\frontend\css\styles.css")) {
    @"
/* ContractAI Main Stylesheet */

:root {
  --primary-color: #4f46e5;
  --primary-hover: #4338ca;
  --secondary-color: #a855f7;
  --text-color: #1f2937;
  --light-bg: #f9fafb;
  --border-color: #e5e7eb;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  color: var(--text-color);
  line-height: 1.5;
}

/* Add your custom styles below */
"@ | Set-Content -Path "$BASE_DIR\ContractAI\frontend\css\styles.css"
}

# Create JS file for frontend
if (-not (Test-Path "$BASE_DIR\ContractAI\frontend\js\main.js")) {
    @"
// ContractAI Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
  console.log('ContractAI application initialized');
  
  // Mobile menu toggle
  const mobileMenuButton = document.querySelector('.md\\:hidden');
  if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', function() {
      const mobileMenu = document.querySelector('.hidden.md\\:flex');
      if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
        mobileMenu.classList.toggle('flex');
        mobileMenu.classList.toggle('flex-col');
        mobileMenu.classList.toggle('absolute');
        mobileMenu.classList.toggle('top-16');
        mobileMenu.classList.toggle('right-0');
        mobileMenu.classList.toggle('bg-white');
        mobileMenu.classList.toggle('w-full');
        mobileMenu.classList.toggle('p-4');
        mobileMenu.classList.toggle('shadow-md');
      }
    });
  }
});
"@ | Set-Content -Path "$BASE_DIR\ContractAI\frontend\js\main.js"
}

Write-Host "Structure creation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Validate the directory structure is correct" -ForegroundColor White
Write-Host "2. Copy any existing code into the new structure" -ForegroundColor White
Write-Host "3. Update import statements if necessary" -ForegroundColor White
Write-Host "4. Verify the application works with the new structure" -ForegroundColor White 