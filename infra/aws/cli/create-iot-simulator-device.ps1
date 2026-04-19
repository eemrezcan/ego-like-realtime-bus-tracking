param(
    [string]$Profile = "eemrezcan",
    [string]$Region = "eu-central-1",
    [string]$AccountId = "775755739642",
    [string]$ThingName = "ego-bus-simulator-device",
    [string]$PolicyName = "ego-bus-simulator-policy"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$policyTemplatePath = Join-Path $repoRoot "infra/aws/iot/simulator-device-policy.json"
$buildDir = Join-Path $repoRoot "build/aws/iot/device"
$resolvedPolicyPath = Join-Path $buildDir "simulator-device-policy.resolved.json"
$certPath = Join-Path $buildDir "device.pem.crt"
$publicKeyPath = Join-Path $buildDir "public.pem.key"
$privateKeyPath = Join-Path $buildDir "private.pem.key"
$aws = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"

New-Item -ItemType Directory -Path $buildDir -Force | Out-Null

$policy = Get-Content -LiteralPath $policyTemplatePath -Raw
$policy = $policy.Replace("<REGION>", $Region)
$policy = $policy.Replace("<ACCOUNT_ID>", $AccountId)
Set-Content -LiteralPath $resolvedPolicyPath -Value $policy -Encoding utf8

& $aws iot describe-thing --thing-name $ThingName --region $Region --profile $Profile 2>$null
if ($LASTEXITCODE -ne 0) {
    & $aws iot create-thing `
        --thing-name $ThingName `
        --region $Region `
        --profile $Profile | Out-Null
}

& $aws iot get-policy --policy-name $PolicyName --region $Region --profile $Profile 2>$null
if ($LASTEXITCODE -ne 0) {
    & $aws iot create-policy `
        --policy-name $PolicyName `
        --policy-document ("file://{0}" -f $resolvedPolicyPath) `
        --region $Region `
        --profile $Profile | Out-Null
}

$certificateDescription = & $aws iot create-keys-and-certificate `
    --set-as-active `
    --certificate-pem-outfile $certPath `
    --public-key-outfile $publicKeyPath `
    --private-key-outfile $privateKeyPath `
    --region $Region `
    --profile $Profile | ConvertFrom-Json

$certificateArn = $certificateDescription.certificateArn
$certificateId = $certificateDescription.certificateId

& $aws iot attach-policy `
    --policy-name $PolicyName `
    --target $certificateArn `
    --region $Region `
    --profile $Profile | Out-Null

& $aws iot attach-thing-principal `
    --thing-name $ThingName `
    --principal $certificateArn `
    --region $Region `
    --profile $Profile | Out-Null

$endpoint = & $aws iot describe-endpoint `
    --endpoint-type iot:Data-ATS `
    --region $Region `
    --profile $Profile `
    --query "endpointAddress" `
    --output text

[pscustomobject]@{
    ThingName = $ThingName
    PolicyName = $PolicyName
    CertificateId = $certificateId
    CertificateArn = $certificateArn
    IotDataEndpoint = $endpoint
    CertificatePath = $certPath
    PrivateKeyPath = $privateKeyPath
    PublicKeyPath = $publicKeyPath
} | ConvertTo-Json -Depth 5
