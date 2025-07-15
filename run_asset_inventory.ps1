# run_asset_inventory.ps1
# Runs asset_inventory.py from this folder against a specified target

$ScriptPath = Join-Path $PSScriptRoot "asset_inventory.py"
$TargetDirectory = Read-Host "Enter full path of target directory to scan"

python $ScriptPath --target "$TargetDirectory"
