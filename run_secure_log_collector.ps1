# PowerShell Launcher for Secure Log Collector

# === Define paths ===
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PythonScript = Join-Path $ScriptDir "secure_log_collector.py"

Write-Host "`n[+] Running Secure Log Collector..." -ForegroundColor Cyan

# === Activate virtualenv if needed ===
# & "$ScriptDir\venv\Scripts\Activate.ps1"

# === Run the Python script ===
python "$PythonScript"

Write-Host "`n[LOG COMPLETE] Secure Log Collector finished." -ForegroundColor Green

