# Read the standardized templates
$headerTemplate = Get-Content "HG-Upload/docmatrixai.com/common/master-header.html" -Raw
$footerTemplate = Get-Content "HG-Upload/docmatrixai.com/common/master-footer.html" -Raw

# Function to calculate relative path to root
function Get-RelativePath {
    param (
        [string]$FilePath
    )
    $depth = ($FilePath -split '/').Count - 3  # Adjusted to account for docmatrixai.com
    if ($depth -lt 0) { return "" }
    return "../" * $depth
}

# Function to format HTML
function Format-HTML {
    param (
        [string]$content
    )
    # Add newlines after closing tags
    $content = $content -replace '>(</[^>]+>)', ">`n`$1"
    # Add newlines after opening tags
    $content = $content -replace '>([^<])', ">`n`$1"
    # Add newlines before opening tags
    $content = $content -replace '(<[^/][^>]*>)', "`n`$1"
    # Add newlines before and after nav and footer sections
    $content = $content -replace '(<nav[^>]*>)', "`n`$1"
    $content = $content -replace '(</nav>)', "`$1`n"
    $content = $content -replace '(<footer[^>]*>)', "`n`$1"
    $content = $content -replace '(</footer>)', "`$1`n"
    # Add indentation
    $lines = $content -split "`n"
    $indent = 0
    $result = @()
    foreach ($line in $lines) {
        $trimmedLine = $line.Trim()
        if ($trimmedLine -match '^</') {
            $indent = [Math]::Max(0, $indent - 1)
        }
        if ($trimmedLine) {
            $result += (" " * ($indent * 4)) + $trimmedLine
        }
        if ($trimmedLine -match '^<[^/][^>]*>$' -and -not $trimmedLine.EndsWith('/>')) {
            $indent++
        }
    }
    return $result -join "`n"
}

# Function to get calculator type from file path
function Get-CalculatorType {
    param (
        [string]$FilePath
    )
    if ($FilePath -match 'ContractAI') { return 'contractai' }
    if ($FilePath -match 'ExpenseDocAI') { return 'expensedocai' }
    if ($FilePath -match 'HR-DocAI') { return 'hrdocai' }
    if ($FilePath -match 'SupplyDocAI') { return 'supplydocai' }
    return $null
}

# Function to check if navigation is outdated
function Test-OutdatedNavigation {
    param (
        [string]$content
    )
    
    # Extract the navigation section
    if ($content -match '<nav[^>]*>.*?</nav>') {
        $navSection = $Matches[0]
        
        # Check for missing dropdown menus
        $hasProductsDropdown = $navSection -match '<li class="nav-item dropdown"[^>]*>.*?<a[^>]*id="productsDropdown"[^>]*>Products</a>'
        $hasResourcesDropdown = $navSection -match '<li class="nav-item dropdown"[^>]*>.*?<a[^>]*id="resourcesDropdown"[^>]*>Resources</a>'
        $hasCompanyDropdown = $navSection -match '<li class="nav-item dropdown"[^>]*>.*?<a[^>]*id="companyDropdown"[^>]*>Company</a>'
        
        # Check for missing dark mode toggle
        $hasDarkModeToggle = $navSection -match '<div class="dark-mode-toggle[^"]*"[^>]*>'
        
        # Check for missing buttons
        $hasSignInButton = $navSection -match '<a[^>]*class="[^"]*btn[^"]*btn-outline-secondary[^"]*"[^>]*>Sign In</a>'
        $hasGetStartedButton = $navSection -match '<a[^>]*class="[^"]*btn[^"]*btn-primary[^"]*"[^>]*>Get Started</a>'
        
        # Check for old logo image
        $hasLogoImage = $navSection -match 'docmatrix-logo\.svg'
        
        # Check for old navigation structure (direct product links)
        $hasOldProductLinks = $navSection -match '<li class="nav-item"><a class="nav-link" href="[^"]*/(HR-DocAI|ContractAI|ExpenseDocAI|SupplyDocAI)/">'
        
        # Return true if any required element is missing or if old elements are present
        $isOutdated = -not ($hasProductsDropdown -and $hasResourcesDropdown -and $hasCompanyDropdown -and 
                           $hasDarkModeToggle -and $hasSignInButton -and $hasGetStartedButton) -or 
                           $hasLogoImage -or $hasOldProductLinks
        
        if ($isOutdated) {
            $missingElements = @()
            if (-not $hasProductsDropdown) { $missingElements += "products dropdown" }
            if (-not $hasResourcesDropdown) { $missingElements += "resources dropdown" }
            if (-not $hasCompanyDropdown) { $missingElements += "company dropdown" }
            if (-not $hasDarkModeToggle) { $missingElements += "dark mode toggle" }
            if (-not $hasSignInButton) { $missingElements += "sign in button" }
            if (-not $hasGetStartedButton) { $missingElements += "get started button" }
            if ($hasLogoImage) { $missingElements += "logo image needs removal" }
            if ($hasOldProductLinks) { $missingElements += "old product links" }
            
            Write-Host "  - Navigation needs update (missing or incorrect: $($missingElements -join ', '))"
        }
        
        return $isOutdated
    }
    
    Write-Host "  - No navigation found"
    return $true
}

# Find all HTML files in the HG-Upload directory
$htmlFiles = Get-ChildItem -Path "HG-Upload" -Filter "*.html" -Recurse

$modifiedCount = 0

foreach ($file in $htmlFiles) {
    Write-Host "Processing $($file.FullName)"
    $wasModified = $false
    
    # Skip template files
    if ($file.FullName -like "*common/standardized-*.html" -or $file.FullName -like "*common/master-*.html") {
        Write-Host "  - Skipping template file"
        continue
    }
    
    # Skip documentation pages
    if ($file.FullName -like "*documentation/*" -and $file.FullName -notlike "*documentation/index.html") {
        Write-Host "  - Skipping documentation page"
        continue
    }
    
    # Read the file content
    $content = Get-Content $file.FullName -Raw

    # Calculate relative path to root
    $relativePath = Get-RelativePath $file.FullName
    Write-Host "  - Relative path: $relativePath"
    
    # Replace BASE_PATH in the templates
    $header = $headerTemplate -replace 'href="/', "href=`"$relativePath"
    $header = $header -replace 'src="/', "src=`"$relativePath"
    $footer = $footerTemplate -replace 'href="/', "href=`"$relativePath"
    $footer = $footer -replace 'src="/', "src=`"$relativePath"
    
    # Update Content Security Policy if present
    if ($content -match '<meta http-equiv="Content-Security-Policy"[^>]*>') {
        $csp = 'default-src ''self''; script-src ''self'' https://cdn.jsdelivr.net ''unsafe-inline''; style-src ''self'' https://cdn.jsdelivr.net https://fonts.googleapis.com ''unsafe-inline''; img-src ''self'' data: https://*.jsdelivr.net; font-src ''self'' https://fonts.gstatic.com; connect-src ''self'';'
        $content = $content -replace '(<meta http-equiv="Content-Security-Policy" content=")[^"]*(")', "`$1$csp`$2"
        $wasModified = $true
        Write-Host "  - Updated Content Security Policy"
    }
    
    # Add required CSS and JS
    $requiredCss = @(
        '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">',
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
        "<link href=`"${relativePath}css/styles.css`" rel=`"stylesheet`">",
        "<link href=`"${relativePath}css/dark-mode.css`" rel=`"stylesheet`">"
    )
    
    $requiredJs = @(
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>',
        "<script src=`"${relativePath}js/main.js`"></script>",
        "<script src=`"${relativePath}js/dark-mode.js`"></script>"
    )
    
    # Add calculator script if needed
    $calculatorType = Get-CalculatorType $file.FullName
    if ($calculatorType -and $content -match 'id="calculator"') {
        $requiredJs += "<script src=`"${relativePath}js/calculator.js`"></script>"
        
        # Add calculator type attribute to the calculator section
        $content = $content -replace '(<section[^>]*id="calculator"[^>]*>)', "`$1`n    <div data-calculator-type=`"$calculatorType`">"
        $content = $content -replace '(</section>)', "    </div>`n`$1"
        $wasModified = $true
        Write-Host "  - Added calculator configuration"
    }
    
    # Add CSS if not present
    foreach ($css in $requiredCss) {
        if (-not $content.Contains($css)) {
            $content = $content -replace '</head>', "`n    $css`n</head>"
            $wasModified = $true
            Write-Host "  - Added CSS: $css"
        }
    }
    
    # Add dark-mode class if not present
    if (-not $content.Contains('class="dark-mode"')) {
        $content = $content -replace '<body', '<body class="dark-mode"'
        $wasModified = $true
        Write-Host "  - Added dark-mode class"
    }
    
    # Add margin-top to first container if header is being added
    if (-not $content.Contains('navbar-expand-lg')) {
        $content = $content -replace '<div class="container">', '<div class="container" style="margin-top: 76px;">'
        $wasModified = $true
        Write-Host "  - Added margin-top to container"
    }
    
    # Check if the file needs header update
    $needsHeaderUpdate = Test-OutdatedNavigation $content
    if ($needsHeaderUpdate) {
        if ($content -match '<nav[^>]*>.*?</nav>') {
            $content = $content -replace '<nav[^>]*>.*?</nav>', $header
            Write-Host "  - Replaced existing header"
        }
        else {
            $content = $content -replace '<body[^>]*>', "`$0`n$header"
            Write-Host "  - Added header"
        }
        $wasModified = $true
    }
    
    # Check if the file needs footer update
    $needsFooterUpdate = $false
    if ($content -match '<footer[^>]*>.*?</footer>') {
        $currentFooter = $Matches[0]
        # Check for missing elements
        $missingElements = @()
        if (-not $currentFooter.Contains('DocMatrix AI. All rights reserved.')) { $missingElements += "copyright notice" }
        if (-not $currentFooter.Contains('Products')) { $missingElements += "products section" }
        if (-not $currentFooter.Contains('Resources')) { $missingElements += "resources section" }
        if (-not $currentFooter.Contains('Company')) { $missingElements += "company section" }
        if (-not $currentFooter.Contains('Legal')) { $missingElements += "legal section" }
        if (-not $currentFooter.Contains('twitter.com/docmatrixai')) { $missingElements += "social links" }
        
        if ($missingElements.Count -gt 0) {
            $needsFooterUpdate = $true
            Write-Host "  - Footer needs update (missing: $($missingElements -join ', '))"
        }
    }
    else {
        $needsFooterUpdate = $true
        Write-Host "  - Footer needs update (no footer found)"
    }
    
    # Replace or add footer
    if ($needsFooterUpdate) {
        if ($content -match '<footer[^>]*>.*?</footer>') {
            $content = $content -replace '<footer[^>]*>.*?</footer>', $footer
            Write-Host "  - Replaced existing footer"
        }
        else {
            $content = $content -replace '</body>', "`n$footer`n</body>"
            Write-Host "  - Added footer"
        }
        $wasModified = $true
    }
    
    # Add JS if not present (before closing body tag)
    foreach ($js in $requiredJs) {
        if (-not $content.Contains($js)) {
            $content = $content -replace '</body>', "`n    $js`n</body>"
            $wasModified = $true
            Write-Host "  - Added JS: $js"
        }
    }
    
    # Write the updated content back to the file if changes were made
    if ($wasModified) {
        try {
            Set-Content -Path $file.FullName -Value $content -NoNewline -Force
            Write-Host "  - Updated successfully"
            $modifiedCount++
        }
        catch {
            Write-Host "  - Error updating file: $_"
        }
    }
    else {
        Write-Host "  - No changes needed"
    }
}

Write-Host "Header and footer update complete! Modified $modifiedCount files." 