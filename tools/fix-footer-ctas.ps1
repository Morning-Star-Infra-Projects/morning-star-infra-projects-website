$rootDir = 'c:\Users\PRABHAKAR\OneDrive\Documents\HEHE-2'
# Get all HTML files recursively, excluding .bak files and .git folder
$pages = Get-ChildItem $rootDir -Recurse -Filter '*.html' | Where-Object {
    $_.Name -notmatch '\.bak$' -and $_.FullName -notmatch '\\.git\\'
}
$old = '<div style="margin-top:16px;display:flex;gap:12px;align-items:center">'
$new = '<div class="footer-contact-ctas">'
$count = 0
foreach ($page in $pages) {
    $content = Get-Content $page.FullName -Raw -Encoding UTF8
    if ($null -ne $content -and $content.Contains($old)) {
        $content = $content.Replace($old, $new)
        [System.IO.File]::WriteAllText($page.FullName, $content, [System.Text.Encoding]::UTF8)
        $count++
        Write-Host "Fixed: $($page.FullName)"
    }
}
Write-Host "Total fixed: $count files."
