$ErrorActionPreference = "Stop"

python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
npm install

Write-Host "Bootstrap complete. Run 'uvicorn apps.api.main:app --reload --port 8000' and 'npm run dev:web'."
