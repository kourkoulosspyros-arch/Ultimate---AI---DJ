@echo off
TITLE Ultimate AI DJ
echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not added to PATH! Please install Python 3.10+.
    pause
    exit /b
)

echo Installing dependencies...
pip install -r requirements.txt

echo Checking FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg is not found in PATH. Audio mixing might fail!
)

echo Launching Ultimate AI DJ...
python main.py
pause
