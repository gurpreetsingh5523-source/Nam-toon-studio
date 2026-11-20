@echo off
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
if exist "C:\msys64\ucrt64\bin\libfribidi-0.dll" set "PATH=C:\msys64\ucrt64\bin;%PATH%"
if not exist ".venv\Scripts\python.exe" (
    where py >nul 2>&1
    if errorlevel 1 (python -m venv .venv) else (py -3 -m venv .venv)
    if errorlevel 1 exit /b 1
)
".venv\Scripts\python.exe" -c "from PIL import features; assert features.check_feature('raqm')" >nul 2>&1
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install --only-binary=:all: -r requirements.txt
    if errorlevel 1 exit /b 1
)
if "%~1"=="--smoke" (
    ".venv\Scripts\python.exe" tools\smoke.py
    exit /b
)
".venv\Scripts\python.exe" server.py %*
