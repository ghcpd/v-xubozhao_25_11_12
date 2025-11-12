<#
PowerShell setup script: creates virtualenv, upgrades pip, installs and upgrades dependencies, pins them into requirements.txt.
#>

$start = (Get-Date).ToString('u')
Write-Host "Start time: $start"

python -m venv .venv
if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
}

python -m pip install --upgrade pip setuptools wheel
if (Test-Path "requirements_old.txt") {
    python -m pip install --upgrade -r requirements.txt
} elseif (Test-Path "requirements_old.txt") {
    Write-Host "Upgrading packages from requirements_old.txt to latest compatible versions"
    $pkgs = Get-Content requirements_old.txt | ForEach-Object { ($_ -split '==')[0] } | Where-Object { $_ -and -not $_.StartsWith('#')} | Sort-Object -Unique
    python -m pip install --upgrade $pkgs
} else {
    Write-Error "requirements_old.txt not found"
    exit 1
}

# Rely on requirements.txt for test tooling versions (avoid broad upgrades to ensure reproducibility)
python -m pip freeze | Sort-Object | Out-File -Encoding utf8 requirements.txt

$end = (Get-Date).ToString('u')
Write-Host "End time: $end"
Write-Host "requirements.txt written - run .\.venv\Scripts\Activate.ps1; ./run_tests.ps1 to run tests"
