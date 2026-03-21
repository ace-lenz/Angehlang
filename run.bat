@echo off
title Angehlang Universe OS - by Longbian Lennon
color 0B
echo.
echo  =====================================
echo   ANGEHLANG v2.1.0 - Universe OS
echo   Created by Longbian Lennon
echo  =====================================
echo.

if "%1"=="" (
    echo  Starting interactive REPL...
    echo  Type .help for commands, .exit to quit.
    echo.
    python "%~dp0core\interpreter.py"
) else (
    echo  Running: %1
    echo.
    python "%~dp0core\interpreter.py" "%~1"
)

pause
