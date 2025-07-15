param (
    [string]$TargetDirectory = ".",
    [string]$OutputFile = "manifest_output.csv"
)

$pythonCommand = "python ./asset_manifest_scanner.py `"$TargetDirectory`" --output `"$OutputFile`""

Write-Host "Running asset integrity scan on: $TargetDirectory"
Invoke-Expression $pythonCommand
Write-Host "Manifest saved to: $OutputFile"
