param(
    [string]$OutputPath = "build/aws/iot/device/AmazonRootCA1.pem"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$resolvedOutputPath = Join-Path $repoRoot $OutputPath
$outputDir = Split-Path -Parent $resolvedOutputPath

New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

Invoke-WebRequest `
    -Uri "https://www.amazontrust.com/repository/AmazonRootCA1.pem" `
    -OutFile $resolvedOutputPath

Write-Host "Amazon Root CA indirildi: $resolvedOutputPath"
