# Ensure execution policy allows running scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Path to Python 3.10
$pythonPath = "C:\Program Files\Python310\python.exe"

# Check if Python 3.10 exists
if (!(Test-Path $pythonPath)) {
    Write-Error "❌ Python 3.10 not found at $pythonPath. Please check the path."
    exit
}

# Create virtual environment
Write-Output "✅ Creating virtual environment 'tf-env'..."
& "$pythonPath" -m venv tf-env

# Activate virtual environment
Write-Output "✅ Activating virtual environment..."
& ".\tf-env\Scripts\Activate.ps1"

# Upgrade pip
Write-Output "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install TensorFlow
Write-Output "📦 Installing TensorFlow..."
pip install tensorflow

# Confirm TensorFlow installed
Write-Output "🔍 TensorFlow version:"
python -c "import tensorflow as tf; print(tf.__version__)"
