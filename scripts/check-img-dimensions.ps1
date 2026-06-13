$files = Get-ChildItem -Recurse -Filter *.html
foreach ($f in $files) {
  $text = Get-Content -Raw $f.FullName
  $matches = [regex]::Matches($text, '<img\\b[^>]*>', 'IgnoreCase')
  foreach ($m in $matches) {
    $tag = $m.Value
    if ($tag -notmatch 'width=' -or $tag -notmatch 'height=') {
      $line = ($text.Substring(0,$m.Index) -split '\r?\n').Count
      Write-Output ($f.FullName + ':' + $line + ':' + $tag)
    }
  }
}
