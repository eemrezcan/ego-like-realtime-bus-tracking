param(
    [string]$Profile = "eemrezcan",
    [string]$Region = "eu-central-1",
    [string]$AccountId = "775755739642",
    [string]$RoleName = "ego-bus-lambda-role",
    [string]$PolicyName = "ego-bus-lambda-inline",
    [string]$StreamName = "ego-bus-telemetry-stream",
    [string]$CurrentStateTable = "bus_current_state",
    [string]$HistoryTable = "telemetry_history"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$trustPolicyPath = Join-Path $repoRoot "infra/aws/iam/lambda-trust-policy.json"
$inlinePolicyTemplatePath = Join-Path $repoRoot "infra/aws/iam/lambda-inline-policy.json"
$buildDir = Join-Path $repoRoot "build/aws/iam"
$resolvedInlinePolicyPath = Join-Path $buildDir "lambda-inline-policy.resolved.json"
$aws = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"

New-Item -ItemType Directory -Path $buildDir -Force | Out-Null

$inlinePolicy = Get-Content -LiteralPath $inlinePolicyTemplatePath -Raw
$inlinePolicy = $inlinePolicy.Replace("<REGION>", $Region)
$inlinePolicy = $inlinePolicy.Replace("<ACCOUNT_ID>", $AccountId)
$inlinePolicy = $inlinePolicy.Replace("<STREAM_NAME>", $StreamName)
$inlinePolicy = $inlinePolicy.Replace("<CURRENT_STATE_TABLE>", $CurrentStateTable)
$inlinePolicy = $inlinePolicy.Replace("<HISTORY_TABLE>", $HistoryTable)
Set-Content -LiteralPath $resolvedInlinePolicyPath -Value $inlinePolicy -Encoding utf8

& $aws iam get-role --role-name $RoleName --profile $Profile 2>$null
if ($LASTEXITCODE -ne 0) {
    & $aws iam create-role `
        --role-name $RoleName `
        --assume-role-policy-document ("file://{0}" -f $trustPolicyPath) `
        --profile $Profile | Out-Null
}

& $aws iam wait role-exists --role-name $RoleName --profile $Profile

& $aws iam put-role-policy `
    --role-name $RoleName `
    --policy-name $PolicyName `
    --policy-document ("file://{0}" -f $resolvedInlinePolicyPath) `
    --profile $Profile | Out-Null

& $aws iam get-role `
    --role-name $RoleName `
    --profile $Profile `
    --query "Role.{RoleName:RoleName,Arn:Arn}" `
    --output json
