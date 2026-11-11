@echo off
title Instalador Agent Orchestrator
echo ===================================================
echo Instalando Ecossistema de Agentes Global...
echo ===================================================

xcopy E I Y .gemini %USERPROFILE%.gemini
xcopy E I Y .agents %USERPROFILE%.agents

echo.
echo [Sucesso] Orquestrador instalado em %USERPROFILE%
echo Para inicializar um projeto, rode o Iniciar_Cerebro.bat na pasta .gemini.
echo.
echo ===================================================
echo Desenvolvido por: Matheus Valpassos
echo GitHub: github.com/matheus-valpassos
echo ===================================================
pause
