$path='c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup\pages\blog.html'
$lines = Get-Content -LiteralPath $path -ErrorAction Stop
if($lines.Count -ge 4315) {
    $head = $lines[0..106]
    $tail = $lines[4314..($lines.Count - 1)]
    $new = $head + $tail
    Set-Content -LiteralPath $path -Value $new -Encoding UTF8
    Write-Output "OK: trimmed. New length: $($new.Count)"
} else {
    Write-Output "ERROR: unexpected file length $($lines.Count)"
}
