$files = Get-ChildItem -Path .\assets\images -Recurse -Include *.png,*.jpg,*.jpeg,*.webp,*.gif -ErrorAction SilentlyContinue
$files = $files | Sort-Object Length -Descending | Select-Object -First 100
foreach ($f in $files) {
  $sizeKB = [math]::Round($f.Length/1024,2)
  Write-Output ($f.FullName + '|' + $sizeKB)
}
