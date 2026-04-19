param(
    [string]$Profile = "eemrezcan",
    [string]$Region = "eu-central-1",
    [string]$FunctionName = "ego-bus-processor",
    [string]$StreamArn = "arn:aws:kinesis:eu-central-1:775755739642:stream/ego-bus-telemetry-stream",
    [int]$BatchSize = 10
)

$ErrorActionPreference = "Stop"

$aws = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"

$existingUuid = & $aws lambda list-event-source-mappings `
    --function-name $FunctionName `
    --event-source-arn $StreamArn `
    --region $Region `
    --profile $Profile `
    --query "EventSourceMappings[0].UUID" `
    --output text

if ($existingUuid -and $existingUuid -ne "None") {
    & $aws lambda get-event-source-mapping `
        --uuid $existingUuid `
        --region $Region `
        --profile $Profile `
        --query "{UUID:UUID,State:State,FunctionArn:FunctionArn,EventSourceArn:EventSourceArn}" `
        --output json
    exit 0
}

& $aws lambda create-event-source-mapping `
    --function-name $FunctionName `
    --event-source-arn $StreamArn `
    --starting-position LATEST `
    --batch-size $BatchSize `
    --region $Region `
    --profile $Profile `
    --query "{UUID:UUID,State:State,FunctionArn:FunctionArn,EventSourceArn:EventSourceArn}" `
    --output json
