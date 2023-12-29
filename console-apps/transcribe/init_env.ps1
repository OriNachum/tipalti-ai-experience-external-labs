
# PowerShell script to initialize Python virtual environment and install packages from requirements.txt

# Create virtual environment
# Check if virtual environment exists, if not create one
if (!(Test-Path .venv)) {
    Write-Output "Creating virtual environment..."
    python3 -m venv .venv
}

# Activate the virtual environment
Write-Output "Activating virtual environment..."
. .venv/Scripts/activate

# Install requirements
pip install -r requirements.txt
