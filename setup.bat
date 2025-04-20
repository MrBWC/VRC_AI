@echo off
echo ===========================================
echo  VRChat AI Agent - Setup with UV
echo ===========================================

:: Check if uv is installed
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] uv is not installed!
    echo Download from: https://github.com/astral-sh/uv
    exit /b 1
)

:: Create virtual environment with uv
echo [1/3] Creating virtual environment...
uv venv .venv

:: Activate virtual environment
echo [2/3] Activating virtual environment...
call .venv\Scripts\activate

:: Install dependencies from requirements.txt
echo [3/3] Installing dependencies...
uv pip install -r requirements.txt

echo.
echo ===========================================
echo  ✅ Setup Complete!
echo ===========================================
echo To start the AI Agent:
echo.
echo   call .venv\Scripts\activate
echo   python main.py
echo.
pause
