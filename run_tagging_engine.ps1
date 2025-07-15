# run_tagging_engine.ps1

param (
    [string]$TargetDirectory = "."
)

# Build Python execution command
$pythonCommand = "python ./logic_tag_writer.py `"$TargetDirectory`""

Write-Host "Running logic tag writer on: $TargetDirectory"
Invoke-Expression $pythonCommand
Write-Host "Tagging complete."
