@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%1.2.py
set COMMAND_FILE=%SCRIPT_DIR%test1.txt

python 1.2.py --startup-script "test1.txt"

pause