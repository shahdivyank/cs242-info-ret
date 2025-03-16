@echo off
:: Deploy backend
echo Deploy backend ...
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%
call venv\Scripts\activate.bat
start /B flask run --host=127.0.0.1 --port=5050

:: Deploy frontend
echo Deploy frontend ...
start /B npm run dev -- --host
pause
