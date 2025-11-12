$start = (Get-Date).ToString('u')
Write-Host "Start time: $start"

if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
}

python -m pytest -v --maxfail=1 --disable-warnings --cov=.

$end = (Get-Date).ToString('u')
Write-Host "End time: $end"
