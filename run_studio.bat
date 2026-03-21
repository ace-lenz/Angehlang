
@echo off
set "SCRIPT_DIR=%~dp0"
set "SUBSTRATE=%SCRIPT_DIR%system\substrate.pvm"
if "%~1"=="" (
    python "%SUBSTRATE%" "%SCRIPT_DIR%boot_god_ai.angeh"
) else (
    python "%SUBSTRATE%" "%~1"
)
pause
