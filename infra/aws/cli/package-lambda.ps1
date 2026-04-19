param(
    [string]$OutputZip = "build/lambda/processor.zip"
)

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$stagingDir = Join-Path $repoRoot "build/lambda/staging"
$zipPath = Join-Path $repoRoot $OutputZip

if (Test-Path $stagingDir) {
    Remove-Item -LiteralPath $stagingDir -Recurse -Force
}

if (Test-Path $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

New-Item -ItemType Directory -Path $stagingDir -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot "processor") -Destination $stagingDir -Recurse -Force
Copy-Item -LiteralPath (Join-Path $repoRoot "simulator") -Destination $stagingDir -Recurse -Force
Copy-Item -LiteralPath (Join-Path $repoRoot "data") -Destination $stagingDir -Recurse -Force

$zipParent = Split-Path -Parent $zipPath
New-Item -ItemType Directory -Path $zipParent -Force | Out-Null

Compress-Archive -Path (Join-Path $stagingDir "*") -DestinationPath $zipPath -Force
Write-Host "Lambda paketi olusturuldu: $zipPath"
