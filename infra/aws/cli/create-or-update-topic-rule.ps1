param(
    [string]$Profile = "eemrezcan",
    [string]$Region = "eu-central-1",
    [string]$RuleName = "ego_bus_telemetry_to_kinesis",
    [string]$Sql = "SELECT * FROM 'ego-sim/v1/bus/telemetry'",
    [string]$RoleArn = "arn:aws:iam::775755739642:role/ego-bus-iot-rule-role",
    [string]$StreamName = "ego-bus-telemetry-stream"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$buildDir = Join-Path $repoRoot "build/aws/iot"
$payloadPath = Join-Path $buildDir "topic-rule-payload.json"
$aws = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"

New-Item -ItemType Directory -Path $buildDir -Force | Out-Null

$payloadObject = @{
    sql = $Sql
    awsIotSqlVersion = "2016-03-23"
    ruleDisabled = $false
    actions = @(
        @{
            kinesis = @{
                roleArn = $RoleArn
                streamName = $StreamName
                partitionKey = '${newuuid()}'
            }
        }
    )
}

$payloadObject | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $payloadPath -Encoding utf8

& $aws iot get-topic-rule --rule-name $RuleName --region $Region --profile $Profile 2>$null
if ($LASTEXITCODE -eq 0) {
    & $aws iot replace-topic-rule `
        --rule-name $RuleName `
        --topic-rule-payload ("file://{0}" -f $payloadPath) `
        --region $Region `
        --profile $Profile | Out-Null
}
else {
    & $aws iot create-topic-rule `
        --rule-name $RuleName `
        --topic-rule-payload ("file://{0}" -f $payloadPath) `
        --region $Region `
        --profile $Profile | Out-Null
}

& $aws iot get-topic-rule `
    --rule-name $RuleName `
    --region $Region `
    --profile $Profile `
    --query "rule.{ruleName:ruleName,sql:sql,ruleDisabled:ruleDisabled}" `
    --output json
