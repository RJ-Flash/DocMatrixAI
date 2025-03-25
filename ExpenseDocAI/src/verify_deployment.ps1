# Verify ExpenseDocAI deployment
param(
    [Parameter(Mandatory=$true)]
    [string]$BaseUrl
)

Write-Host "Verifying ExpenseDocAI deployment at $BaseUrl..."

# Function to make HTTP request with error handling
function Invoke-ApiRequest {
    param(
        [string]$Endpoint,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [object]$Body = $null
    )
    
    try {
        $params = @{
            Uri = "$BaseUrl$Endpoint"
            Method = $Method
            Headers = $Headers
            UseBasicParsing = $true
        }
        
        if ($Body) {
            $params.Body = $Body | ConvertTo-Json
            $params.ContentType = "application/json"
        }
        
        $response = Invoke-WebRequest @params
        return @{
            Success = $true
            StatusCode = $response.StatusCode
            Content = $response.Content | ConvertFrom-Json
        }
    }
    catch {
        return @{
            Success = $false
            StatusCode = $_.Exception.Response.StatusCode.value__
            Error = $_.Exception.Message
        }
    }
}

# Check health endpoint
Write-Host "`nChecking health endpoint..."
$health = Invoke-ApiRequest -Endpoint "/health/"
if ($health.Success) {
    Write-Host "Health check successful!" -ForegroundColor Green
    Write-Host "Status: $($health.Content.status)"
    Write-Host "Components:"
    $health.Content.components | Format-Table
}
else {
    Write-Host "Health check failed: $($health.Error)" -ForegroundColor Red
    exit 1
}

# Get authentication token
Write-Host "`nGetting authentication token..."
$auth = Invoke-ApiRequest -Endpoint "/api/v1/auth/token/" -Method "POST" -Body @{
    username = $env:EXPENSE_DOC_USER
    password = $env:EXPENSE_DOC_PASSWORD
}
if (-not $auth.Success) {
    Write-Host "Authentication failed: $($auth.Error)" -ForegroundColor Red
    exit 1
}
$token = $auth.Content.access

# Test document upload
Write-Host "`nTesting document upload..."
$headers = @{
    "Authorization" = "Bearer $token"
}

# Create test image
$testImage = New-Object System.Drawing.Bitmap(1000, 1000)
$graphics = [System.Drawing.Graphics]::FromImage($testImage)
$graphics.Clear([System.Drawing.Color]::White)
$font = New-Object System.Drawing.Font("Arial", 12)
$brush = [System.Drawing.Brushes]::Black
$graphics.DrawString("Test Receipt`nAmount: $100.00`nDate: 2024-02-20", $font, $brush, 10, 10)
$testImagePath = "test_receipt.png"
$testImage.Save($testImagePath, [System.Drawing.Imaging.ImageFormat]::Png)

# Upload document
$form = @{
    file = Get-Item $testImagePath
    process_now = "true"
}
$upload = Invoke-ApiRequest -Endpoint "/api/v1/documents/upload/" -Method "POST" -Headers $headers -Form $form
if ($upload.Success) {
    Write-Host "Document upload successful!" -ForegroundColor Green
    $documentId = $upload.Content.document.id
    
    # Wait for processing
    Write-Host "Waiting for document processing..."
    $maxAttempts = 12
    $attempt = 0
    $processed = $false
    
    while ($attempt -lt $maxAttempts -and -not $processed) {
        $status = Invoke-ApiRequest -Endpoint "/api/v1/documents/$documentId/" -Headers $headers
        if ($status.Content.status -eq "COMPLETED") {
            $processed = $true
            Write-Host "Document processed successfully!" -ForegroundColor Green
            Write-Host "Extracted entries:"
            $status.Content.entries | Format-Table
        }
        elseif ($status.Content.status -eq "ERROR") {
            Write-Host "Document processing failed: $($status.Content.error_message)" -ForegroundColor Red
            break
        }
        else {
            Write-Host "Processing... (attempt $($attempt + 1)/$maxAttempts)"
            Start-Sleep -Seconds 5
            $attempt++
        }
    }
    
    if (-not $processed) {
        Write-Host "Document processing timed out" -ForegroundColor Yellow
    }
}
else {
    Write-Host "Document upload failed: $($upload.Error)" -ForegroundColor Red
}

# Clean up
Remove-Item $testImagePath

Write-Host "`nDeployment verification completed!" 