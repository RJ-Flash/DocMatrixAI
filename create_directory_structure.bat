@echo off
echo Creating DocMatrix AI project directory structure...

REM Set the base directory to the current workspace
set BASE_DIR=%CD%

echo Current directory: %BASE_DIR%

REM Create frontend missing files (already exist, but ensuring structure is complete)
echo Creating Frontend files...
mkdir "%BASE_DIR%\ContractAI\frontend\css" 2>nul
mkdir "%BASE_DIR%\ContractAI\frontend\js" 2>nul
mkdir "%BASE_DIR%\ContractAI\frontend\images" 2>nul

REM Create AI Models directory
echo Creating AI Models directory...
mkdir "%BASE_DIR%\ContractAI\app\ai\models" 2>nul
mkdir "%BASE_DIR%\ContractAI\app\ai\models\bert" 2>nul
mkdir "%BASE_DIR%\ContractAI\app\ai\models\gpt" 2>nul
mkdir "%BASE_DIR%\ContractAI\app\ai\models\custom" 2>nul

REM Create model initialization files if they don't exist
if not exist "%BASE_DIR%\ContractAI\app\ai\models\__init__.py" (
    echo """
AI models package for ContractAI.
This package contains the machine learning models used for contract analysis.
""" > "%BASE_DIR%\ContractAI\app\ai\models\__init__.py"
)

if not exist "%BASE_DIR%\ContractAI\app\ai\models\bert\__init__.py" (
    echo """
BERT-based models for contract analysis.
""" > "%BASE_DIR%\ContractAI\app\ai\models\bert\__init__.py"
)

if not exist "%BASE_DIR%\ContractAI\app\ai\models\gpt\__init__.py" (
    echo """
GPT-based models for contract analysis.
""" > "%BASE_DIR%\ContractAI\app\ai\models\gpt\__init__.py"
)

if not exist "%BASE_DIR%\ContractAI\app\ai\models\custom\__init__.py" (
    echo """
Custom models for contract analysis.
""" > "%BASE_DIR%\ContractAI\app\ai\models\custom\__init__.py"
)

REM Create model implementation files
if not exist "%BASE_DIR%\ContractAI\app\ai\models\bert\clause_extractor.py" (
    echo """
from transformers import BertTokenizer, BertForSequenceClassification
import torch

class BertClauseExtractor:
    def __init__(self, model_path='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        
    def extract_clauses(self, text):
        # Implementation for clause extraction using BERT
        pass
""" > "%BASE_DIR%\ContractAI\app\ai\models\bert\clause_extractor.py"
)

if not exist "%BASE_DIR%\ContractAI\app\ai\models\gpt\text_analyzer.py" (
    echo """
import openai

class GPTTextAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
        
    def analyze_text(self, text, prompt=None):
        # Implementation for text analysis using GPT
        pass
""" > "%BASE_DIR%\ContractAI\app\ai\models\gpt\text_analyzer.py"
)

REM Create Shared Resources
echo Creating Shared Resources...
mkdir "%BASE_DIR%\shared\branding\logos" 2>nul
mkdir "%BASE_DIR%\shared\branding\themes" 2>nul
mkdir "%BASE_DIR%\shared\components\ui" 2>nul
mkdir "%BASE_DIR%\shared\components\widgets" 2>nul
mkdir "%BASE_DIR%\shared\utils\ai-core" 2>nul
mkdir "%BASE_DIR%\shared\utils\common" 2>nul

REM Create shared component files
if not exist "%BASE_DIR%\shared\components\ui\header.js" (
    echo """
// Shared header component for DocMatrix AI products
class Header {
    constructor(options = {}) {
        this.title = options.title || 'DocMatrix AI';
        this.logo = options.logo || '/shared/branding/logos/default.svg';
    }
    
    render() {
        // Implementation for rendering header
        return `<header class="docmatrix-header">
            <img src="${this.logo}" alt="${this.title} Logo" />
            <h1>${this.title}</h1>
        </header>`;
    }
}

export default Header;
""" > "%BASE_DIR%\shared\components\ui\header.js"
)

if not exist "%BASE_DIR%\shared\components\ui\footer.js" (
    echo """
// Shared footer component for DocMatrix AI products
class Footer {
    constructor(options = {}) {
        this.copyright = options.copyright || `© ${new Date().getFullYear()} DocMatrix AI`;
        this.links = options.links || [];
    }
    
    render() {
        // Implementation for rendering footer
        return `<footer class="docmatrix-footer">
            <p>${this.copyright}</p>
        </footer>`;
    }
}

export default Footer;
""" > "%BASE_DIR%\shared\components\ui\footer.js"
)

REM Create Infrastructure
echo Creating Infrastructure directories...
mkdir "%BASE_DIR%\infrastructure\kubernetes\deployments" 2>nul
mkdir "%BASE_DIR%\infrastructure\kubernetes\services" 2>nul
mkdir "%BASE_DIR%\infrastructure\kubernetes\configmaps" 2>nul
mkdir "%BASE_DIR%\infrastructure\terraform\modules" 2>nul
mkdir "%BASE_DIR%\infrastructure\terraform\environments" 2>nul
mkdir "%BASE_DIR%\infrastructure\terraform\variables" 2>nul
mkdir "%BASE_DIR%\infrastructure\monitoring\grafana" 2>nul
mkdir "%BASE_DIR%\infrastructure\monitoring\prometheus" 2>nul
mkdir "%BASE_DIR%\infrastructure\monitoring\alerts" 2>nul

REM Create Kubernetes deployment files
if not exist "%BASE_DIR%\infrastructure\kubernetes\deployments\contractai.yaml" (
    echo """
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
""" > "%BASE_DIR%\infrastructure\kubernetes\deployments\contractai.yaml"
)

if not exist "%BASE_DIR%\infrastructure\kubernetes\services\contractai.yaml" (
    echo """
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
""" > "%BASE_DIR%\infrastructure\kubernetes\services\contractai.yaml"
)

REM Create Terraform files
if not exist "%BASE_DIR%\infrastructure\terraform\main.tf" (
    echo """
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
""" > "%BASE_DIR%\infrastructure\terraform\main.tf"
)

REM Create Future Product Placeholders
echo Creating Future Product Placeholders...
mkdir "%BASE_DIR%\HR-DocAI\docs" 2>nul
mkdir "%BASE_DIR%\HR-DocAI\src" 2>nul
if not exist "%BASE_DIR%\HR-DocAI\README.md" (
    echo # HR Document Compliance Management > "%BASE_DIR%\HR-DocAI\README.md"
    echo. >> "%BASE_DIR%\HR-DocAI\README.md"
    echo HR-DocAI is an AI-powered solution for managing HR documents and ensuring compliance with regulations. >> "%BASE_DIR%\HR-DocAI\README.md"
    echo. >> "%BASE_DIR%\HR-DocAI\README.md"
    echo ## Features >> "%BASE_DIR%\HR-DocAI\README.md"
    echo. >> "%BASE_DIR%\HR-DocAI\README.md"
    echo - Automated document classification >> "%BASE_DIR%\HR-DocAI\README.md"
    echo - Compliance checking against regulations >> "%BASE_DIR%\HR-DocAI\README.md"
    echo - Employee data extraction and validation >> "%BASE_DIR%\HR-DocAI\README.md"
)

mkdir "%BASE_DIR%\SupplyDocAI\docs" 2>nul
mkdir "%BASE_DIR%\SupplyDocAI\src" 2>nul
if not exist "%BASE_DIR%\SupplyDocAI\README.md" (
    echo # Supply Chain Documentation Automation > "%BASE_DIR%\SupplyDocAI\README.md"
    echo. >> "%BASE_DIR%\SupplyDocAI\README.md"
    echo SupplyDocAI streamlines supply chain documentation processes using AI to extract, validate, and manage critical information. >> "%BASE_DIR%\SupplyDocAI\README.md"
    echo. >> "%BASE_DIR%\SupplyDocAI\README.md"
    echo ## Features >> "%BASE_DIR%\SupplyDocAI\README.md"
    echo. >> "%BASE_DIR%\SupplyDocAI\README.md"
    echo - Purchase order analysis >> "%BASE_DIR%\SupplyDocAI\README.md"
    echo - Shipping document verification >> "%BASE_DIR%\SupplyDocAI\README.md"
    echo - Inventory reconciliation >> "%BASE_DIR%\SupplyDocAI\README.md"
)

mkdir "%BASE_DIR%\ExpenseDocAI\docs" 2>nul
mkdir "%BASE_DIR%\ExpenseDocAI\src" 2>nul
if not exist "%BASE_DIR%\ExpenseDocAI\README.md" (
    echo # Expense Report Automation > "%BASE_DIR%\ExpenseDocAI\README.md"
    echo. >> "%BASE_DIR%\ExpenseDocAI\README.md"
    echo ExpenseDocAI automates the processing of expense reports, receipts, and invoices using advanced AI techniques. >> "%BASE_DIR%\ExpenseDocAI\README.md"
    echo. >> "%BASE_DIR%\ExpenseDocAI\README.md"
    echo ## Features >> "%BASE_DIR%\ExpenseDocAI\README.md"
    echo. >> "%BASE_DIR%\ExpenseDocAI\README.md"
    echo - Receipt OCR and data extraction >> "%BASE_DIR%\ExpenseDocAI\README.md"
    echo - Expense categorization >> "%BASE_DIR%\ExpenseDocAI\README.md"
    echo - Policy compliance checking >> "%BASE_DIR%\ExpenseDocAI\README.md"
)

REM Create Configuration Files
echo Creating Configuration Files...
mkdir "%BASE_DIR%\ContractAI\config" 2>nul
mkdir "%BASE_DIR%\ContractAI\scripts\setup" 2>nul
mkdir "%BASE_DIR%\ContractAI\scripts\deployment" 2>nul

if not exist "%BASE_DIR%\ContractAI\config\development.yaml" (
    echo """
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
""" > "%BASE_DIR%\ContractAI\config\development.yaml"
)

if not exist "%BASE_DIR%\ContractAI\config\production.yaml" (
    echo """
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
""" > "%BASE_DIR%\ContractAI\config\production.yaml"
)

if not exist "%BASE_DIR%\ContractAI\config\staging.yaml" (
    echo """
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
""" > "%BASE_DIR%\ContractAI\config\staging.yaml"
)

REM Create setup and deployment scripts
if not exist "%BASE_DIR%\ContractAI\scripts\setup\install_dependencies.bat" (
    echo """
@echo off
echo Installing ContractAI dependencies...
pip install -r ../../requirements.txt
echo Dependencies installed successfully.
""" > "%BASE_DIR%\ContractAI\scripts\setup\install_dependencies.bat"
)

if not exist "%BASE_DIR%\ContractAI\scripts\deployment\deploy_to_kubernetes.bat" (
    echo """
@echo off
echo Deploying ContractAI to Kubernetes...
kubectl apply -f ../../../infrastructure/kubernetes/deployments/contractai.yaml
kubectl apply -f ../../../infrastructure/kubernetes/services/contractai.yaml
echo ContractAI deployed successfully.
""" > "%BASE_DIR%\ContractAI\scripts\deployment\deploy_to_kubernetes.bat"
)

REM Create CSS file for frontend
if not exist "%BASE_DIR%\ContractAI\frontend\css\styles.css" (
    echo """
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
""" > "%BASE_DIR%\ContractAI\frontend\css\styles.css"
)

REM Create JS file for frontend
if not exist "%BASE_DIR%\ContractAI\frontend\js\main.js" (
    echo """
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
""" > "%BASE_DIR%\ContractAI\frontend\js\main.js"
)

echo Structure creation complete!
echo.
echo Next steps:
echo 1. Validate the directory structure is correct
echo 2. Copy any existing code into the new structure
echo 3. Update import statements if necessary
echo 4. Verify the application works with the new structure 