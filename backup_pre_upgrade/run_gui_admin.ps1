# Super Enhanced Research Agent - Run GUI as Administrator
# PowerShell script to run the research agent GUI with administrator privileges

param(
    [switch]$NoAdminCheck
)

Write-Host "==========================================="
Write-Host " Super Enhanced Research Agent"
Write-Host " Running GUI as Administrator"
Write-Host "==========================================="
Write-Host ""

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not $NoAdminCheck) {
    if (Test-Administrator) {
        Write-Host "Running with administrator privileges..." -ForegroundColor Green
    } else {
        Write-Host "Requesting administrator privileges..." -ForegroundColor Yellow

        # Relaunch as administrator
        $scriptPath = $MyInvocation.MyCommand.Path
        $arguments = "-NoAdminCheck"

        try {
            Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -File `"$scriptPath`" $arguments" -Verb RunAs -Wait
            exit
        } catch {
            Write-Host "Failed to request administrator privileges: $($_.Exception.Message)" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
}

# Run the GUI
Write-Host "Starting Super Enhanced Research Agent GUI..." -ForegroundColor Cyan
try {
    # Ensure we're in the correct directory
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $scriptDir

    & python run_desktop_gui.py
} catch {
    Write-Host "Error running GUI: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "GUI session ended."
Read-Host "Press Enter to exit"