param(
    [string]$Profile = "eemrezcan",
    [string]$Region = "eu-central-1",
    [string]$AccountId = "775755739642",
    [string]$RoleName = "ego-bus-iot-rule-role",
    [string]$PolicyName = "ego-bus-iot-rule-inline",
    [string]$StreamName = "ego-bus-telemetry-stream"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$trustPolicyPath = Join-Path $repoRoot "infra/aws/iam/iot-rule-trust-policy.json"
$buildDir = Join-Path $repoRoot "build/aws/iot"
$policyPath = Join-Path $buildDir "iot-rule-inline-policy.json"
$aws = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"

New-Item -ItemType Directory -Path $buildDir -Force | Out-Null

$policyObject = @{
    Version = "2012-10-17"
    Statement = @(
        @{
            Sid = "AllowKinesisPutRecord"
            Effect = "Allow"
            Action = @("kinesis:PutRecord")
            Resource = "arn:aws:kinesis:$Region`:$AccountId`:stream/$StreamName"
        }
    )
}

$policyObject | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $policyPath -Encoding utf8

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
    --policy-document ("file://{0}" -f $policyPath) `
    --profile $Profile | Out-Null

& $aws iam get-role `
    --role-name $RoleName `
    --profile $Profile `
    --query "Role.{RoleName:RoleName,Arn:Arn}" `
    --output json
