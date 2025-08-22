# Create a virtual environment (if missing), install dependencies, and start the FastAPI server.
$venvPath = Join-Path $PSScriptRoot ".venv"

if (-not (Test-Path $venvPath)) {
	Write-Host "Creating virtual environment at $venvPath"
	python -m venv $venvPath
}

$activate = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
	Write-Error "Could not find virtual environment activate script at $activate"
	exit 1
}

Write-Host "Activating virtual environment"
. $activate

Write-Host "Upgrading pip and installing requirements (if needed)"
python -m pip install --upgrade pip
pip install -r (Join-Path $PSScriptRoot 'requirements.txt')

Write-Host "Starting server on 0.0.0.0:8000"
python -m uvicorn server:app --host 0.0.0.0 --port 8000
