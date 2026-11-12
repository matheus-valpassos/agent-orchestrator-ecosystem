@echo off
title Instalador - Agent Orchestrator Ecosystem
chcp 65001 >nul
cls

echo ========================================================================
echo   🧠 INSTALADOR AUTOMÁTICO - AGENT ORCHESTRATOR ECOSYSTEM
echo ========================================================================
echo.
echo Instalando o ecossistema de agentes global no seu computador...
echo Destino: %USERPROFILE%
echo.

set "SCRIPT_DIR=%~dp0"

:: 1. Criar pastas necessárias no perfil do usuário
if not exist "%USERPROFILE%\.agents" mkdir "%USERPROFILE%\.agents"
if not exist "%USERPROFILE%\.gemini" mkdir "%USERPROFILE%\.gemini"
if not exist "%USERPROFILE%\.claude" mkdir "%USERPROFILE%\.claude"

:: 2. Copiar .agents (Skills, Agents e Scripts)
echo [*] Instalando .agents (Skills e Scripts do Orquestrador)...
robocopy "%SCRIPT_DIR%.agents" "%USERPROFILE%\.agents" /E /NFL /NDL /NJH /NJS /nc /ns /np >nul 2>nul
if %ERRORLEVEL% GEQ 8 (
    xcopy /E /I /Y /H /K "%SCRIPT_DIR%.agents\*" "%USERPROFILE%\.agents\" >nul 2>nul
)

:: 3. Copiar .gemini (GEMINI.md, init_memory.py, Iniciar_Cerebro.bat)
echo [*] Instalando .gemini (Instruções e Inicializador de Memória)...
robocopy "%SCRIPT_DIR%.gemini" "%USERPROFILE%\.gemini" /E /NFL /NDL /NJH /NJS /nc /ns /np >nul 2>nul
if %ERRORLEVEL% GEQ 8 (
    xcopy /E /I /Y /H /K "%SCRIPT_DIR%.gemini\*" "%USERPROFILE%\.gemini\" >nul 2>nul
)

:: 4. Configurar compatibilidade universal com outros LLMs (Claude Code, Cursor, etc.)
echo [*] Configurando compatibilidade universal com LLMs (Claude, Cursor, Gemini)...
copy /Y "%SCRIPT_DIR%.gemini\GEMINI.md" "%USERPROFILE%\.claude\CLAUDE.md" >nul 2>nul
copy /Y "%SCRIPT_DIR%.gemini\GEMINI.md" "%USERPROFILE%\CLAUDE.md" >nul 2>nul
copy /Y "%SCRIPT_DIR%.gemini\GEMINI.md" "%USERPROFILE%\.cursorrules" >nul 2>nul

:: 5. Facilitador: copiar Iniciar_Cerebro.bat para locais convenientes
copy /Y "%SCRIPT_DIR%.gemini\Iniciar_Cerebro.bat" "%USERPROFILE%\Iniciar_Cerebro.bat" >nul 2>nul
if exist "%USERPROFILE%\Desktop" (
    copy /Y "%SCRIPT_DIR%.gemini\Iniciar_Cerebro.bat" "%USERPROFILE%\Desktop\Iniciar_Cerebro.bat" >nul 2>nul
)

:: 6. Verificar instalação do Python e instalar dependências
echo.
echo [*] Verificando ambiente Python...
set "PYTHON_CMD="
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=python"
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set "PYTHON_CMD=py"
    )
)

if defined PYTHON_CMD (
    echo [+] Python detectado com sucesso.
    echo [*] Instalando/atualizando dependências necessárias (PyYAML)...
    %PYTHON_CMD% -m pip install pyyaml --quiet >nul 2>nul
    echo [*] Executando varredura inicial do registro de skills (Auto-Discovery)...
    %PYTHON_CMD% "%USERPROFILE%\.agents\skills\agent-orchestrator\scripts\scan_registry.py" >nul 2>nul
    echo [+] Registro de skills construído e pronto para uso!
) else (
    echo [!] AVISO: Python 3 não foi detectado no PATH do sistema.
    echo     Os arquivos foram copiados com sucesso, mas para habilitar o
    echo     auto-discovery de skills e orquestração automática:
    echo     1. Baixe o Python em: https://www.python.org/downloads/
    echo     2. IMPORTANTE: Marque a caixa "Add Python to PATH" durante a instalação.
)

echo.
echo ========================================================================
echo   [SUCESSO] Ecossistema instalado e configurado globalmente!
echo ========================================================================
echo.
echo Como inicializar seu projeto:
echo  1. Acesse a pasta onde você quer criar ou abrir seu projeto.
echo  2. Dê duplo clique no atalho 'Iniciar_Cerebro.bat' (na sua Área de Trabalho
echo     ou em %%USERPROFILE%%\.gemini\Iniciar_Cerebro.bat)
echo     ou digite no terminal do projeto: python "%USERPROFILE%\.gemini\init_memory.py"
echo  3. Pronto! A pasta .memory/ e as proteções de CI/CD serão criadas no projeto.
echo.
echo Compatibilidade Universal Ativada:
echo  - Claude Code (CLI)              -> ~/.claude/CLAUDE.md
echo  - Google Antigravity / Gemini    -> ~/.gemini/GEMINI.md
echo  - Cursor IDE                     -> ~/.cursorrules
echo  - Windsurf, Copilot, ChatGPT     -> Consulte o MANUAL_DE_USO.md
echo.
echo ========================================================================
echo Desenvolvido com 🧠 por Matheus Valpassos* 
echo https://github.com/matheus-valpassos
echo Mtech - Purr. Ecosystem
echo ========================================================================
echo.
pause
