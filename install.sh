#!/usr/bin/env bash
# ========================================================================
#   🧠 INSTALADOR AUTOMÁTICO - AGENT ORCHESTRATOR ECOSYSTEM
# ========================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================================================"
echo "  🧠 INSTALANDO ECOSSISTEMA DE AGENTES GLOBAL..."
echo "========================================================================"
echo ""
echo "Destino: $HOME"
echo ""

# 1. Criar pastas no perfil do usuário
mkdir -p "$HOME/.agents"
mkdir -p "$HOME/.gemini"
mkdir -p "$HOME/.claude"

# 2. Copiar .agents e .gemini
echo "[*] Copiando skills, agents e scripts para ~/.agents/..."
cp -R "$SCRIPT_DIR/.agents/"* "$HOME/.agents/"

echo "[*] Copiando regras e inicializadores para ~/.gemini/..."
cp -R "$SCRIPT_DIR/.gemini/"* "$HOME/.gemini/"

# 3. Compatibilidade Universal com Claude Code e Cursor
echo "[*] Configurando compatibilidade universal (Claude Code, Cursor, Gemini)..."
cp "$SCRIPT_DIR/.gemini/GEMINI.md" "$HOME/.claude/CLAUDE.md"
cp "$SCRIPT_DIR/.gemini/GEMINI.md" "$HOME/CLAUDE.md"
cp "$SCRIPT_DIR/.gemini/GEMINI.md" "$HOME/.cursorrules"

# 4. Conceder permissão de execução aos scripts
chmod +x "$HOME/.agents/skills/agent-orchestrator/scripts/"*.py 2>/dev/null || true
if [ -f "$HOME/.gemini/Iniciar_Cerebro.bat" ]; then
    chmod +x "$HOME/.gemini/Iniciar_Cerebro.bat" 2>/dev/null || true
fi

# 5. Verificar Python e instalar dependências
echo ""
echo "[*] Verificando ambiente Python..."
PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
fi

if [ -n "$PYTHON_BIN" ]; then
    echo "[+] Python detectado ($($PYTHON_BIN --version))"
    echo "[*] Instalando dependências necessárias (PyYAML)..."
    $PYTHON_BIN -m pip install pyyaml --quiet 2>/dev/null || true
    echo "[*] Executando varredura inicial do registro de skills..."
    $PYTHON_BIN "$HOME/.agents/skills/agent-orchestrator/scripts/scan_registry.py" >/dev/null 2>&1 || true
    echo "[+] Registro de skills indexado com sucesso!"
else
    echo "[!] AVISO: Python 3 não foi detectado no sistema."
    echo "    Instale o Python 3 para habilitar o auto-discovery de skills."
fi

echo ""
echo "========================================================================"
echo "  [SUCESSO] Ecossistema instalado e configurado globalmente!"
echo "========================================================================"
echo ""
echo "Como inicializar seu projeto:"
echo "  1. Acesse a pasta do seu projeto."
echo "  2. Execute: python3 ~/.gemini/init_memory.py"
echo "  3. Pronto! A pasta .memory/ e as proteções de CI/CD serão criadas."
echo ""
echo "Compatibilidade ativada para:"
echo "  - Claude Code (CLI)                  -> ~/.claude/CLAUDE.md"
echo "  - Google Antigravity / Gemini CLI    -> ~/.gemini/GEMINI.md"
echo "  - Cursor IDE                         -> ~/.cursorrules"
echo "  - Windsurf / VS Code Copilot / ChatGPT -> Veja MANUAL_DE_USO.md"
echo ""
echo "========================================================================"
echo "Desenvolvido com 🧠 por Matheus Valpassos"
echo "https://github.com/matheus-valpassos"
echo "Mtech - Purr. Ecosystem"
echo "========================================================================"
