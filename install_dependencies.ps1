# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python and try again."
    exit 1
}

# Optionally, create and activate a virtual environment
# python -m venv venv
# .\venv\Scripts\Activate

# Install dependencies using pip
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

Write-Host "Dependencies installed successfully!"
