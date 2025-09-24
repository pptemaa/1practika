@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%1.2.py
set COMMAND_FILE=%SCRIPT_DIR%test2.txt

python 1.2.py --vfs-path "test_folder" --startup-script "test2.txt"

pause