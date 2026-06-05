$root = "c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup"
Get-ChildItem -Path $root -Recurse -Include *.html | ForEach-Object {
  $path = $_.FullName
  $s = Get-Content -LiteralPath $path -Raw -ErrorAction SilentlyContinue
  if(-not $s) { return }
  $orig = $s
  # Normalize src to absolute /assets/images/... for Morning-Star-Infra-Projects-Header-Logo.*
  $s = [regex]::Replace($s, '(<img[^>]*?)src=("|\')(?:(?:\.{1,3}\/)?assets\/images\/)?(Morning-Star-Infra-Projects-Header-Logo(?:[-_\d]*?)\.(?:webp|jpeg|jpg))("|\')', '$1src="/assets/images/$3"', 'IgnoreCase')
  # Ensure image is wrapped with anchor to '/'
  $s = [regex]::Replace($s, '(?i)(<a[^>]*href=("|\')/?("|\')?[^>]*>\s*)?(<img[^>]*Morning-Star-Infra-Projects-Header-Logo[^>]*>)(\s*</a>)?', '<a href="/">$4</a>')
  if($s -ne $orig){ Set-Content -LiteralPath $path -Value $s -Encoding UTF8; Write-Output "Updated: $path" }
}
