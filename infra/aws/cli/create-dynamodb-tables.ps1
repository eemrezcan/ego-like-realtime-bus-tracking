param(
    [string]$Region = "eu-central-1",
    [string]$CurrentStateTable = "bus_current_state",
    [string]$HistoryTable = "telemetry_history"
)

aws dynamodb create-table `
    --region $Region `
    --table-name $CurrentStateTable `
    --attribute-definitions AttributeName=bus_id,AttributeType=S `
    --key-schema AttributeName=bus_id,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST

aws dynamodb create-table `
    --region $Region `
    --table-name $HistoryTable `
    --attribute-definitions AttributeName=bus_id,AttributeType=S AttributeName=timestamp,AttributeType=S `
    --key-schema AttributeName=bus_id,KeyType=HASH AttributeName=timestamp,KeyType=RANGE `
    --billing-mode PAY_PER_REQUEST
