pip install scapy

# Set window title
$Host.UI.RawUI.WindowTitle = "Packet Sniffer"

# Check for Administrator rights
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Warning "This script must be run as Administrator to capture packets!"
    pause
    exit
}

# Run the Python sniffer
Write-Host "`n[+] Launching packet_sniffer.py...`n"
python ".\packet_sniffer.py"
