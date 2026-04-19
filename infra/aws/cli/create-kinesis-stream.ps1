param(
    [string]$Region = "eu-central-1",
    [string]$StreamName = "ego-bus-telemetry-stream",
    [int]$ShardCount = 1
)

aws kinesis create-stream `
    --region $Region `
    --stream-name $StreamName `
    --shard-count $ShardCount
