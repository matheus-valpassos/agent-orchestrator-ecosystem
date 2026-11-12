@echo off
title Agent Memory Setup - Purr. Ecosystem
chcp 65001 >nul

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python "%~dp0init_memory.py"
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        py "%~dp0init_memory.py"
    ) else (
        echo [ERRO] Python não foi encontrado no PATH do sistema.
        echo Por favor, instale o Python em https://www.python.org/downloads/ e marque "Add Python to PATH".
        pause
    )
)
