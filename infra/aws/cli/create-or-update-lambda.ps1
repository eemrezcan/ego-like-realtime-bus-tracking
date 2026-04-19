param(
    [string]$Profile = "eemrezcan",
    [string]$Region = "eu-central-1",
    [string]$FunctionName = "ego-bus-processor",
    [string]$RoleArn,
    [string]$Runtime = "python3.12",
    [string]$CurrentStateTable = "bus_current_state",
    [string]$HistoryTable = "telemetry_history"
)

$ErrorActionPreference = "Stop"

if (-not $RoleArn) {
    throw "RoleArn zorunludur."
}

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$packageScript = Join-Path $repoRoot "infra/aws/cli/package-lambda.ps1"
$zipPath = Join-Path $repoRoot "build/lambda/processor.zip"
$aws = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"
$environmentArg = "Variables={PROCESSOR_STORAGE_MODE=dynamodb,DDB_CURRENT_STATE_TABLE=$CurrentStateTable,DDB_HISTORY_TABLE=$HistoryTable}"

& $packageScript

& $aws lambda get-function --function-name $FunctionName --region $Region --profile $Profile 2>$null
if ($LASTEXITCODE -eq 0) {
    & $aws lambda update-function-code `
        --function-name $FunctionName `
        --zip-file ("fileb://{0}" -f $zipPath) `
        --region $Region `
        --profile $Profile | Out-Null

    & $aws lambda update-function-configuration `
        --function-name $FunctionName `
        --handler "processor.lambda_handler.lambda_handler" `
        --runtime $Runtime `
        --role $RoleArn `
        --timeout 30 `
        --memory-size 256 `
        --environment $environmentArg `
        --region $Region `
        --profile $Profile | Out-Null
}
else {
    & $aws lambda create-function `
        --function-name $FunctionName `
        --runtime $Runtime `
        --handler "processor.lambda_handler.lambda_handler" `
        --role $RoleArn `
        --zip-file ("fileb://{0}" -f $zipPath) `
        --timeout 30 `
        --memory-size 256 `
        --environment $environmentArg `
        --region $Region `
        --profile $Profile | Out-Null
}

& $aws lambda wait function-active-v2 --function-name $FunctionName --region $Region --profile $Profile

& $aws lambda get-function `
    --function-name $FunctionName `
    --region $Region `
    --profile $Profile `
    --query "Configuration.{FunctionName:FunctionName,Runtime:Runtime,State:State,LastModified:LastModified,FunctionArn:FunctionArn}" `
    --output json
