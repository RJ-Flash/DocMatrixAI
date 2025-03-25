# Load environment variables
$env:HOSTGATOR_FTP_USER = "LND-RJG@ixk.hjg.temporary.site"
$env:HOSTGATOR_FTP_PASS = "x7`$F@9m!Qr#8bT2^"
$env:HOSTGATOR_FTP_HOST = "ftp.ixk.hjg.temporary.site"

# Create logs directory if it doesn't exist
$logDir = "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

# Setup logging
$logFile = Join-Path $logDir "deploy-$(Get-Date -Format 'yyyy-MM-dd-HH-mm-ss').log"
function Write-Log {
    param($Message, $Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage
}

Write-Log "Starting deployment..." "INFO"

# Verify required files exist
$requiredFiles = @(
    "./docmatrixai.com/index.html",
    "./docmatrixai.com/.htaccess",
    "./api.docmatrixai.com/app.js",
    "./api.docmatrixai.com/.htaccess"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Log "Required file not found: $file" "ERROR"
        exit 1
    }
}

# Create temporary script file
$scriptPath = "upload.txt"
@"
option batch abort
option confirm off
open ftp://$($env:HOSTGATOR_FTP_USER):$($env:HOSTGATOR_FTP_PASS)@$($env:HOSTGATOR_FTP_HOST)/
cd /public_html
put -r ./docmatrixai.com/* /
cd /api.docmatrixai.com
put -r ./api.docmatrixai.com/* /
exit
"@ | Out-File -FilePath $scriptPath -Encoding ASCII

try {
    # Deploy using FTP
    Write-Log "Uploading files..." "INFO"
    
    # Try to find ftp.exe in various locations
    $ftpPaths = @(
        "C:\Windows\System32\ftp.exe",
        "C:\Windows\SysWOW64\ftp.exe"
    )
    
    $ftpExe = $ftpPaths | Where-Object { Test-Path $_ } | Select-Object -First 1
    
    if (-not $ftpExe) {
        Write-Log "FTP executable not found!" "ERROR"
        exit 1
    }
    
    & $ftpExe -s:$scriptPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Log "Files deployed successfully!" "INFO"
        
        # Verify deployment
        Write-Log "Verifying deployment..." "INFO"
        $urls = @(
            "https://docmatrixai.com",
            "https://api.docmatrixai.com/health"
        )
        
        foreach ($url in $urls) {
            try {
                $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
                if ($response.StatusCode -eq 200) {
                    Write-Log "Successfully verified $url" "INFO"
                } else {
                    Write-Log "Warning: $url returned status code $($response.StatusCode)" "WARN"
                }
            } catch {
                Write-Log "Error verifying $url : $_" "ERROR"
            }
        }
    } else {
        Write-Log "Error deploying files!" "ERROR"
        exit 1
    }
} catch {
    Write-Log "Deployment failed: $_" "ERROR"
    exit 1
} finally {
    # Clean up
    if (Test-Path $scriptPath) {
        Remove-Item $scriptPath
    }
}

Write-Log "Deployment completed successfully!" "INFO"
Write-Log "Website: https://docmatrixai.com" "INFO"
Write-Log "API: https://api.docmatrixai.com" "INFO"
