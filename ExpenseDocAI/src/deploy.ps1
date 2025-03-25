# Deployment script for HostGator
param(
    [Parameter(Mandatory=$true)]
    [string]$HostGatorUsername,
    
    [Parameter(Mandatory=$true)]
    [string]$HostGatorHost,
    
    [Parameter(Mandatory=$true)]
    [string]$RemotePath
)

# Run tests first
Write-Host "Running tests..."
.\run_tests.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Tests failed. Aborting deployment."
    exit 1
}

# Collect static files
Write-Host "Collecting static files..."
python manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Error "Static file collection failed."
    exit 1
}

# Create deployment package
Write-Host "Creating deployment package..."
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$packageName = "expense_doc_$timestamp.zip"

# Exclude unnecessary files
$excludeList = @(
    "*.pyc",
    "__pycache__",
    "*.log",
    "venv",
    ".git",
    ".pytest_cache",
    "htmlcov",
    "*.zip"
)

# Create zip file
Compress-Archive -Path * -DestinationPath $packageName -Force
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create deployment package."
    exit 1
}

# Upload to HostGator
Write-Host "Uploading to HostGator..."
$scpCommand = "scp $packageName $HostGatorUsername@$HostGatorHost`:$RemotePath"
Invoke-Expression $scpCommand
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to upload package to HostGator."
    exit 1
}

# SSH into HostGator and deploy
$sshCommands = @"
cd $RemotePath
unzip -o $packageName
rm $packageName
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
touch dispatch.fcgi
deactivate
"@

$sshCommand = "ssh $HostGatorUsername@$HostGatorHost '$sshCommands'"
Invoke-Expression $sshCommand
if ($LASTEXITCODE -ne 0) {
    Write-Error "Deployment failed."
    exit 1
}

# Clean up local package
Remove-Item $packageName

Write-Host "Deployment completed successfully!" 