@echo off
title Codex API Config Tool

python --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Install from: https://www.python.org/downloads/
    echo Check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python detected.
python --version
echo.

echo ========================================
echo   Starting config wizard...
echo ========================================
echo.

python "%~dp0codex_config.py"

echo.
pause
