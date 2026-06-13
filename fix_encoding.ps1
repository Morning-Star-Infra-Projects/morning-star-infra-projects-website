# PowerShell script to fix double-encoded UTF-8 characters
# This replaces the Python fix_double_encoding.py functionality

$htmlFiles = Get-ChildItem -Path "." -Filter "*.html" -Recurse

$badPatterns = @(
    @{ pattern = 'â€"'; replacement = '–'; name = 'en-dash' }
    @{ pattern = 'â€"'; replacement = '—'; name = 'em-dash' }
    @{ pattern = 'â€¦'; replacement = '…'; name = 'ellipsis' }
    @{ pattern = 'Â©'; replacement = '©'; name = 'copyright' }
    @{ pattern = 'â‚¹'; replacement = '₹'; name = 'rupee-sign' }
    @{ pattern = 'â†''; replacement = '↑'; name = 'uparrow' }
    @{ pattern = 'â€º'; replacement = '›'; name = 'single-right-angle' }
    @{ pattern = 'Ã©'; replacement = 'é'; name = 'e-acute' }
    @{ pattern = 'Ã—'; replacement = '×'; name = 'multiplication' }
    @{ pattern = 'â€˜'; replacement = '''; name = 'left-single-quote' }
    @{ pattern = 'â€™'; replacement = '''; name = 'right-single-quote' }
    @{ pattern = 'â€œ'; replacement = '"'; name = 'left-double-quote' }
    @{ pattern = 'â€'; replacement = '"'; name = 'right-double-quote' }
    @{ pattern = 'â"€'; replacement = '─'; name = 'horizontal-line' }
    @{ pattern = 'â„¢'; replacement = '™'; name = 'trademark' }
    @{ pattern = 'DÃ©cor'; replacement = 'Décor'; name = 'Decor-accent' }
)

$fixedCount = 0
$fixedFiles = @()

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Encoding Fix Report" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $originalContent = $content
    $changesMade = $false
    
    foreach ($pattern in $badPatterns) {
        if ($content -match [regex]::Escape($pattern.pattern)) {
            $content = $content -replace [regex]::Escape($pattern.pattern), $pattern.replacement
            $changesMade = $true
        }
    }
    
    if ($changesMade) {
        # Backup original file
        $backupPath = $file.FullName + ".bak"
        if (-not (Test-Path $backupPath)) {
            Copy-Item -Path $file.FullName -Destination $backupPath
        }
        
        # Write fixed content
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        $fixedCount++
        $fixedFiles += $file.FullName
        
        Write-Host "✓ Fixed: $($file.FullName)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Files processed: $($htmlFiles.Count)"
Write-Host "Files fixed: $fixedCount" -ForegroundColor Green
Write-Host ""

if ($fixedFiles.Count -gt 0) {
    Write-Host "Fixed files:" -ForegroundColor Yellow
    foreach ($file in $fixedFiles) {
        Write-Host "  • $(Split-Path -Leaf $file)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Backup files created with .bak extension" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
