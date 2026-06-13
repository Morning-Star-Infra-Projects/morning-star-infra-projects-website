param(
  [string]$SourceDir = "assets/images",
  [string]$OutDir = "assets/images/optimized",
  [int[]]$Sizes = @(1600,1200,800,400),
  [int]$Quality = 80
)

 $magickCmd = (Get-Command magick -ErrorAction SilentlyContinue)
if (-not $magickCmd) {
  $fallback = 'C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe'
  if (Test-Path $fallback) { $magickCmd = $fallback } else {
    Write-Error "ImageMagick 'magick' not found in PATH and fallback not present. Install ImageMagick or use the Node script."
    exit 1
  }
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Get-ChildItem -Path $SourceDir -Recurse -Include *.png,*.jpg,*.jpeg,*.webp,*.gif -File | ForEach-Object {
  $src = $_.FullName
  $rel = Resolve-Path -Path $src | ForEach-Object { $_.Path.Substring((Get-Item -Path $SourceDir).FullName.Length).TrimStart('\') }
  $destFolder = Join-Path $OutDir (Split-Path $rel -Parent)
  if (-not (Test-Path $destFolder)) { New-Item -ItemType Directory -Path $destFolder -Force | Out-Null }
    foreach ($w in $Sizes) {
    $base = [IO.Path]::Combine($destFolder, ([IO.Path]::GetFileNameWithoutExtension($src) + "-" + $w))
    $webp = $base + '.webp'
    & $magickCmd convert $src -resize ${w}x -quality $Quality $webp
    $avif = $base + '.avif'
    & $magickCmd convert $src -resize ${w}x -quality $Quality $avif
  }
}

Write-Output "Done. Optimized images are in $OutDir"
