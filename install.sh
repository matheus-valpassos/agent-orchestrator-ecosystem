#!/bin/bash
echo "==================================================="
echo " Instalando Ecossistema de Agentes Global..."
echo "==================================================="

cp -r .gemini ~/
cp -r .agents ~/

echo ""
echo "[Sucesso] Orquestrador instalado em ~/"
echo "Para inicializar um projeto, execute: python3 ~/.gemini/init_memory.py"