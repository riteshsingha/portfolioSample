# ──────────────────────────────────────────────────────────────
# Run the portfolio backend on Windows (PowerShell).
# Usage:   .\run.ps1
# ──────────────────────────────────────────────────────────────

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "venv not found. Creating it..." -ForegroundColor Yellow
    python -m venv venv
}

. .\venv\Scripts\Activate.ps1

Write-Host "Installing requirements..." -ForegroundColor Cyan
pip install --upgrade pip | Out-Null
pip install -r requirements.txt

if (-not (Test-Path ".\.env")) {
    Write-Host ".env not found. Copy .env.example to .env and fill in your SMTP credentials." -ForegroundColor Red
    exit 1
}

Write-Host "Starting FastAPI on http://127.0.0.1:8000 ..." -ForegroundColor Green
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
