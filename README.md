# Agent Orchestrator Ecosystem 🧠

Um ecossistema de agentes IA focado em **Zero Intervenção**, **Isolamento Estrito de Contexto** e **Economia Máxima de Tokens**. 

Em vez de usar prompts gigantes que alucinam e gastam milhares de tokens, este ecossistema delega o roteamento de skills para scripts Python locais e injeta regras de negócio (Clean Code, Segurança, Performance) de forma fracionada.

## 🚀 Como Instalar (Global)

O sistema vive na sua pasta de usuário (`~/.gemini` e `~/.agents`), permitindo que você o chame em qualquer projeto.

**Windows:**
Dê um duplo clique no arquivo `install.bat`.

**Linux / Mac:**
```bash
chmod +x install.sh
./install.sh
```

🛠️ Como Usar (Por Projeto)
Vá até a pasta do projeto onde você deseja programar.

Inicialize o cérebro local daquele projeto rodando o script:

Windows: Clique no atalho ~/.gemini/Iniciar_Cerebro.bat

Linux/Mac: python3 ~/.gemini/init_memory.py

O script criará a pasta .memory/ (com regras de Rollback, Segurança e CI/CD injetadas).

Abra o seu Cursor, Claude Code ou terminal do projeto, e dê o comando usando o orquestrador. Exemplo:

"Crie os modelos de banco de dados para um blog."

O Orquestrador lerá a memória local, escolherá o subagente certo e aplicará os padrões arquiteturais sem conversas fiadas.