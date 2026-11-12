import os
from pathlib import Path

def create_memory_structure():
    print("="*65)
    print(" 🧠 Inicializador de Memória Fracionada + Security Gate")
    print("="*65)
    
    target_dir = input("\nArraste a pasta do seu projeto para cá ou cole o caminho\n(pressione ENTER para usar a pasta atual):\n> ").strip('"\' ')
    if not target_dir:
        path = Path.cwd()
    else:
        path = Path(target_dir)
    
    if not path.exists() or not path.is_dir():
        print("\n[Erro] Diretório não encontrado.")
        return

    memory_dir = path / ".memory"
    patterns_dir = memory_dir / "patterns"
    github_workflows_dir = path / ".github" / "workflows"
    
    try:
        # Criando diretórios
        memory_dir.mkdir(parents=True, exist_ok=True)
        patterns_dir.mkdir(parents=True, exist_ok=True)
        github_workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # ==========================================
        # 1. GITHUB ACTIONS (CI/CD Security Gate)
        # ==========================================
        security_gate_file = github_workflows_dir / "security-gate.yml"
        security_gate_file.write_text("""name: Security Gate (Pré-Deploy)

on:
  push:
    branches: [ main, master, production ]
  pull_request:
    branches: [ main, master, production ]

permissions:
  contents: read
  security-events: write

jobs:
  # 1. Varredura de Segredos no Código e Histórico
  secret-scan:
    name: Varredura de Segredos (Gitleaks)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do código
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Executar Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # 2. Análise Estática de Código (SAST) - Multi-linguagem
  sast-analysis:
    name: Análise Estática de Código (Semgrep)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Executar Semgrep (OWASP Top 10 & Segredos)
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/security-audit
            p/secrets

  # 3. Auditoria de Dependências (Auto-detecta Node.js e/ou Python)
  dependency-audit:
    name: Auditoria de Dependências
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Auditar pacotes Node.js (se existir package-lock.json)
        if: hashFiles('**/package-lock.json') != ''
        run: |
          find . -name "package-lock.json" -not -path "*/node_modules/*" -execdir npm audit --audit-level=high \\;

      - name: Auditar pacotes Python (se existir requirements.txt ou pyproject.toml)
        if: hashFiles('**/requirements.txt', '**/pyproject.toml') != ''
        run: |
          pip install pip-audit
          find . -name "requirements.txt" -exec pip-audit -r {} \\;

  # 4. Auditoria de Contêiner Docker (se existir Dockerfile)
  container-scan:
    name: Segurança de Dockerfile e Imagem (Trivy)
    runs-on: ubuntu-latest
    if: hashFiles('**/Dockerfile') != ''
    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Auditar configurações do Dockerfile (Misconfigurations)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  # 5. Verificação Dinâmica de Headers HTTP e SSL (Opcional pós-staging)
  headers-check:
    name: Validação de Headers HTTP (Staging)
    runs-on: ubuntu-latest
    # Só executa se a variável STAGING_URL estiver configurada no repositório
    if: vars.STAGING_URL != ''
    steps:
      - name: Verificar Headers Obrigatórios
        run: |
          echo "Verificando headers em ${{ vars.STAGING_URL }}..."
          HEADERS=$(curl -s -I -L "${{ vars.STAGING_URL }}")
          
          check_header() {
            if ! echo "$HEADERS" | grep -qi "$1"; then
              echo "❌ FALHA: Header obrigatório ausente -> $1"
              exit 1
            else
              echo "✅ OK: $1 presente"
            fi
          }

          check_header "Strict-Transport-Security"
          check_header "X-Content-Type-Options"
          check_header "X-Frame-Options"
""", encoding="utf-8")

        # ==========================================
        # 2. FRACIONAMENTO (Padrões de Memória)
        # ==========================================
        security_file = patterns_dir / "security-rules.md"
        security_file.write_text("""# Padrões de Segurança e Privacidade (Zero Trust)

> **Diretriz Operacional:** Este documento define regras obrigatórias para geração, revisão e refatoração de código em qualquer stack ou infraestrutura. Nenhuma entrega deve violar estes controles.

## 1. Privacidade, Dados e Auditoria
- **Minimização e Retenção:** Colete e armazene apenas dados estritamente necessários para a regra de negócio, aplicando políticas automáticas de descarte ou anonimização.
- **Criptografia:** Proteja dados em trânsito (**TLS 1.2+**) e em repouso (**AES-256**). Utilize apenas algoritmos e bibliotecas criptográficas consolidadas (ex: Argon2id, HMAC-SHA256) e ativamente mantidas.
- **Logs Limpos e Auditoria:** Nunca grave senhas, tokens, chaves de API ou dados pessoais (PII) em logs ou respostas de erro. Registre eventos críticos de auditoria (falhas de login, alterações de permissão, acesso a dados sensíveis) de forma estruturada e sem dados sensíveis.

## 2. Autenticação, Sessão e Controle de Acesso
- **Autenticação Robusta:** Exija autenticação forte (MFA, tokens JWT/JWS de curta duração e rotação segura de sessões) em qualquer endpoint protegido.
- **Armazenamento Seguro de Sessão:** Armazene tokens de sessão exclusivamente em cookies com flags **`HttpOnly`**, **`Secure`** e **`SameSite=Strict`** (ou `Lax` quando necessário para fluxos OAuth), proibindo o uso de `localStorage` ou `sessionStorage` para credenciais.
- **Autorização Granular e Anti-IDOR:** Aplique Controle de Acesso Baseado em Papéis (**RBAC**) e isolamento estrito de dados por inquilino/usuário (via **Row-Level Security** no banco quando suportado e obrigatoriamente na camada de serviço/API). Sempre valide no servidor se o usuário autenticado é o legítimo proprietário do recurso solicitado (prevenção contra **IDOR**).
- **Zero Hardcode e Isolamento de Chaves:** Nunca insira segredos no código. Separe estritamente variáveis públicas (expostas ao navegador) de variáveis privadas (credenciais de banco, chaves de API e segredos de assinatura), carregando-as via variáveis de ambiente ou cofres de segredos.

## 3. Codificação Segura e Defesa de Perímetro (API-First)
- **Validação Estrita de Entrada:** Valide tipo, formato, esquema e tamanho de todo *payload* no servidor (ex: Pydantic, Zod, Bean Validation) e sanitize saídas para bloquear **SQL Injection**, **XSS** e **Command Injection**.
- **Queries Parametrizadas:** Utilize exclusivamente ORMs seguros ou *prepared statements*. Jamais concatene strings diretamente em consultas de banco de dados.
- **Resiliência e Controle de Abuso:** Implemente **Rate Limiting** por IP e por usuário em endpoints críticos (login, formulários, webhooks) e valide assinaturas criptográficas (ex: **HMAC-SHA256** com *nonces*/timestamps) em integrações e rotas de servidor.
- **Headers e CORS:** Configure políticas restritivas de CORS (apenas origens autorizadas) e cabeçalhos de segurança HTTP obrigatórios (**CSP**, **HSTS**, **X-Frame-Options**, **X-Content-Type-Options**, **Permissions-Policy**).

## 4. Cadeia de Suprimentos e Infraestrutura
- **Integridade de Pacotes:** Mantenha dependências atualizadas, utilize arquivos de trava (`lockfiles`) e audite vulnerabilidades conhecidas regularmente (`npm audit`, `pip-audit`, `bandit` ou equivalentes da linguagem).
- **Prevenção de Vazamento no Git:** Garanta que arquivos `.env`, certificados e chaves locais estejam no `.gitignore` e valide a ausência de segredos antes de qualquer *commit*.
- **Menor Privilégio e Isolamento de Rede:** Conceda a serviços, contêineres, bancos de dados e usuários apenas as permissões mínimas indispensáveis. Nunca exponha portas de bancos de dados ou serviços internos diretamente à internet pública.
""", encoding="utf-8")

        engineering_file = patterns_dir / "engineering-rules.md"
        engineering_file.write_text("""# Regras de Engenharia, Segurança e Clean Code

## 1. Arquitetura e Design de Código
- **Princípios Base:** Aplicar estritamente **SOLID**, **DRY** (extrair lógica repetida), **KISS** (evitar *overengineering*) e **YAGNI** (não criar código especulativo).
- **Modularidade:** Manter clara separação de responsabilidades entre módulos, classes e funções.

## 2. Segurança e Privacidade (Zero Trust)
- **Minimização e Retenção:** Coletar apenas dados estritamente necessários e aplicar políticas de descarte.
- **Criptografia:** Proteger dados sensíveis em trânsito (TLS) e em repouso/banco usando algoritmos e bibliotecas consolidadas.
- **Autenticação e Acesso:** Implementar MFA/tokens fortes e controle baseado em papéis (RBAC). Zero credenciais hardcoded (usar `.env`).
- **Higienização de Entradas:** Validar e sanitizar todos os inputs do usuário contra SQL Injection, XSS e Command Injection.
- **Dependências:** Utilizar apenas bibliotecas e componentes atualizados e auditados.

## 3. Performance e Processamento de Dados
- **Eficiência:** Evitar loops desnecessários; priorizar vetorização e processamento em *chunks*.
- **Recursos:** Aplicar gestão otimizada de memória, serialização leve e compressão de dados.
- **Escalabilidade:** Usar processamento paralelo, particionamento de datasets e *profiling* para eliminar gargalos, equilibrando performance e legibilidade.

## 4. Testes e Qualidade (TDD)
- **Cobertura:** Seguir Desenvolvimento Orientado a Testes (TDD) com testes unitários abrangentes (`pytest` ou `unittest`) validando regras críticas e casos de borda.
- **Segurança Contínua:** Submeter alterações críticas a revisão de código e verificação de vulnerabilidades.

## 5. Documentação e Comentários
- **Docstrings:** Uso obrigatório de *docstrings* claras em todas as classes, métodos e funções.
- **Comentários Pontuais:** Comentar apenas lógicas de negócio complexas, *workarounds* (explicando o motivo), referências a documentações externas e marcadores `TODO`.
""", encoding="utf-8")

        performance_file = patterns_dir / "performance-rules.md"
        performance_file.write_text("""# Padrões de Performance e Escalabilidade

## 1. Processamento Eficiente de Dados
- **Loops e Vetorização:** Evite loops e iterações desnecessários; priorize operações vetorizadas (ex: NumPy, Pandas ou operações nativas em lote).
- **Grandes Volumes:** Processe datasets extensos em *chunks* (lotes menores) ou *streams* para não estourar a memória RAM.
- **Serialização e Compressão:** Utilize formatos binários/compactos (ex: Parquet, Protobuf, MsgPack) e compressão (Gzip, Zstd) para tráfego e armazenamento de dados.

## 2. Gestão de Memória e Diagnóstico
- **Profiling Obrigatório:** Faça *profiling* de CPU e memória antes de otimizar cegamente para identificar gargalos reais.
- **Otimização de Memória:** Libere referências não utilizadas, evite cópias profundas (*deep copies*) desnecessárias e prefira geradores (*generators*) em vez de listas completas em memória.

## 3. Concorrência e Escalabilidade
- **Paralelismo:** Aplique processamento paralelo (multiprocessing/threads) para tarefas *CPU-bound* e programação assíncrona (`async/await`) para operações *I/O-bound* (APIs, disco, rede).
- **Banco de Dados e Storage:** Utilize indexação adequada, paginação baseada em cursor, particionamento de tabelas/dados e estratégias de cache para reduzir latência.
- **Equilíbrio:** Nunca sacrifique a legibilidade e a manutenibilidade do código por micro-otimizações irrelevantes.
""", encoding="utf-8")

        # ==========================================
        # 3. ÍNDICE ARQUITETURAL
        # ==========================================
        arch_file = memory_dir / "ARCHITECTURE.md"
        arch_file.write_text("""# Índice Arquitetural do Projeto

## Stack do Projeto (Marque com 'x' e apague o restante para economizar tokens)
- **Frontend:** [ ] React/Next.js | [ ] Vue/Nuxt | [ ] HTMX/Alpine | [ ] Tailwind CSS | [ ] Bootstrap
- **Mobile:** [ ] React Native/Expo | [ ] Flutter | [ ] Kotlin (Android) | [ ] Swift (iOS)
- **Backend:** [ ] Python/Django | [ ] Python/FastAPI | [ ] Node.js/Express | [ ] C++/ASM | [ ] C#/.NET
- **Database:** [ ] PostgreSQL | [ ] SQL Server (MSSQL) | [ ] MongoDB | [ ] Redis | [ ] SQLite
- **Infra/Deploy:** [ ] Docker | [ ] Linux VPS/Nginx | [ ] AWS/GCP | [ ] Railway/Render/Supabase

## Padrões Específicos (Leia apenas se a tarefa exigir)
- **Segurança e Privacidade:** Leia `.memory/patterns/security-rules.md`
- **Performance e Otimização:** Leia `.memory/patterns/performance-rules.md`
- **Clean Code e TDD:** Leia `.memory/patterns/engineering-rules.md`

## Comandos Úteis
| Tarefa | Comando (File-Scoped) |
|---|---|
| Run/Dev | `[preencher]` |
| Testes | `[preencher]` |
| Lint | `[preencher]` |
""", encoding="utf-8")

        # ==========================================
        # 4. CONTROLE DE ESTADO
        # ==========================================
        state_file = memory_dir / "STATE.md"
        state_file.write_text("""# Estado Atual

## Tarefa Atual
- [ ] Inicializar o projeto.

## Rollback Point
- N/A
""", encoding="utf-8")

        # ==========================================
        # 5. CHECKLIST DE SEGURANÇA (Agnóstico)
        # ==========================================
        checklist_file = memory_dir / "pre-deploy-security-checklist.md"
        checklist_file.write_text("""# Checklist de Segurança Pré-Deploy (Agnóstico)

> **Regra de Liberação:** Nenhum código ou infraestrutura deve ser promovido para produção com itens críticos pendentes neste checklist.

## 1. Gestão de Segredos e Configurações
- [ ] **Zero Segredos no Código:** O repositório foi varrido (ex: `gitleaks`, `trufflehog`) e não contém chaves de API, senhas, strings de conexão ou certificados.
- [ ] **Arquivos Ignorados:** `.env`, chaves privadas (`.pem`, `.key`) e arquivos de configuração local estão listados no `.gitignore`.
- [ ] **Separação de Ambiente:** As credenciais de produção são totalmente distintas das usadas em desenvolvimento e homologação.
- [ ] **Isolamento de Variáveis:** Variáveis injetadas no bundle do frontend (client-side) contêm apenas URLs públicas ou chaves públicas, nunca segredos administrativos.
- [ ] **Modo Debug Desativado:** Flags de depuração (`DEBUG=False`, `NODE_ENV=production`) estão configuradas para não expor *stack traces* ou informações internas em erros.

## 2. Autenticação, Sessão e Autorização
- [ ] **Cookies Blindados:** Tokens de sessão são enviados via cookies com as flags `HttpOnly`, `Secure` e `SameSite=Strict` (ou `Lax` para OAuth).
- [ ] **Expiração e Rotação:** Tokens JWT/sessões possuem tempo de expiração curto e mecanismos funcionais de renovação (*refresh*) e revogação no logout.
- [ ] **Testes de IDOR (Quebra de Controle de Acesso):** Foi testado e confirmado que um Usuário A não consegue ler, alterar ou deletar recursos do Usuário B apenas trocando o ID na URL ou no *payload*.
- [ ] **Validação de Papéis (RBAC):** Rotas administrativas bloqueiam requisições de usuários comuns diretamente no servidor (retorno `403 Forbidden`), não apenas ocultando botões na interface.

## 3. API, Entradas e Defesa de Perímetro
- [ ] **Validação de Schema:** Todos os endpoints validam tipos, formatos e limites de tamanho de entrada no servidor antes de processar dados.
- [ ] **Proteção contra Injeção:** Todas as consultas ao banco usam ORM ou *prepared statements*; não há concatenação de strings em queries.
- [ ] **Rate Limiting Ativo:** Endpoints sensíveis (login, cadastro, recuperação de senha, envio de e-mails e webhooks) possuem limite de requisições por IP/usuário.
- [ ] **CORS Restritivo:** A política de CORS permite requisições apenas dos domínios oficiais do frontend (sem `Access-Control-Allow-Origin: *` em rotas autenticadas).
- [ ] **Headers de Segurança:** As respostas HTTP incluem `Strict-Transport-Security` (HSTS), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` (ou `SAMEORIGIN`) e `Content-Security-Policy` (CSP).

## 4. Banco de Dados e Rede (VPS / Cloud / Contêineres)
- [ ] **Isolamento de Porta:** O banco de dados e serviços internos (ex: Redis) não estão expostos à internet pública (acessíveis apenas via rede privada, VPC ou `localhost`).
- [ ] **Menor Privilégio no Banco:** A aplicação conecta-se ao banco usando um usuário dedicado com permissões apenas de leitura/escrita nas tabelas necessárias (nunca usando `root` ou `postgres`).
- [ ] **TLS / HTTPS Forçado:** Todo o tráfego HTTP é redirecionado automaticamente para HTTPS com certificado válido (TLS 1.2 ou 1.3).
- [ ] **Firewall Configurado (se VPS):** Apenas as portas estritamente necessárias (ex: 80, 443 e porta SSH customizada com chave pública) estão abertas.
- [ ] **Backups Automatizados:** Rotinas de backup criptografado do banco de dados estão ativas e foram testadas.

## 5. Dependências e Artefatos
- [ ] **Auditoria de Vulnerabilidades:** O comando de auditoria da stack (`npm audit`, `pip-audit`, etc.) foi executado sem falhas críticas ou altas pendentes.
- [ ] **Lockfiles Atualizados:** Os arquivos de trava de versão (`package-lock.json`, `poetry.lock`, etc.) estão sincronizados e commitados.
- [ ] **Contêineres Mínimos (se Docker):** A imagem roda com usuário não-root (`USER node` ou `USER appuser`) e utiliza base enxuta (ex: `alpine` ou `slim`).
""", encoding="utf-8")

        # ==========================================
        # 6. INSTRUÇÕES DO COORDENADOR (LLM Agnostic)
        # ==========================================
        tier1_prompt = """# Orquestrador de Desenvolvimento (Meta-Skill)

Você atua como o Coordenador Técnico (Tier 1). Seu objetivo absoluto é economizar tokens executando "Offloading" de decisões para scripts Python e garantindo isolamento cirúrgico de contexto.

## 1. Princípios de Alta Eficiência
- **Zero Intervenção:** NUNCA adivinhe qual subagente usar. Confie cegamente no output dos scripts de match.
- **Compressão de Contexto:** NUNCA envie o código completo de um arquivo para um subagente se apenas uma parte precisar de alteração. Envie apenas os snippets (trechos) relevantes.
- **Comunicação Estrita:** A comunicação inter-agentes deve ser APENAS Código Raw (Diffs) ou JSON. É terminantemente proibido gerar saudações, explicações textuais ou frases de transição.

## 2. Leitura de Memória (Estado Local)
Antes de iniciar qualquer ação, leia silenciosamente a pasta local do projeto:
- `.memory/ARCHITECTURE.md` (Para restrições, stack e convenções).
- `.memory/STATE.md` (Para identificar a tarefa atual e o último estado estável).

## 3. Workflow Obrigatório de Roteamento
Para processar qualquer solicitação do usuário, rode a varredura no terminal (usando cache MD5):

`python "~/.agents/skills/agent-orchestrator/scripts/scan_registry.py" && python "~/.agents/skills/agent-orchestrator/scripts/match_skills.py" "<resumo_da_solicitacao>"`

### 3.1. Interpretação e Execução
Com base no retorno do terminal, execute a ação correspondente:

*   **Se Match = 1 Skill:** 
    - Carregue o arquivo indicado e delegue.
    - Formato do comando: `Use: <skill-name> | Target: <caminho_do_arquivo> | Task: <instrucao_curta>`
*   **Se Match >= 2 Skills (Orquestração):**
    - Defina o padrão e agende no terminal:
      - **Sequencial:** `python "~/.agents/skills/agent-orchestrator/scripts/orchestrate.py" --mode sequential --skills <skill1,skill2> --query "<pedido>"`
      - **Paralelo:** `python "~/.agents/skills/agent-orchestrator/scripts/orchestrate.py" --mode parallel --skills <skill1,skill2> --query "<pedido>"`
      - **Primário + Suporte:** `python "~/.agents/skills/agent-orchestrator/scripts/orchestrate.py" --mode primary-support --skills <skill1,skill2> --query "<pedido>"`

## 4. Finalização e Segurança (Constitutional Check)
- **Log Automático:** Após qualquer alteração de código bem-sucedida, acione o `context-scribe` passando estritamente o *diff* da mudança para atualizar o `.memory/STATE.md`.
- **Rollback Imediato:** Se uma alteração quebrar o sistema ou falhar, leia a tag `Último estado estável` no `STATE.md` e reverta as alterações IMEDIATAMENTE antes de tentar debugar. A recuperação tem prioridade sobre a análise.

---

Desenvolvido com 🧠 por Matheus Valpassos* 
[github.com/matheus-valpassos](https://github.com/matheus-valpassos)  
Mtech - Purr. Ecosystem
"""
        claude_file = path / "CLAUDE.md"
        if not claude_file.exists():
            claude_file.write_text(tier1_prompt, encoding="utf-8")

        cursor_file = path / ".cursorrules"
        if not cursor_file.exists():
            cursor_file.write_text(tier1_prompt, encoding="utf-8")

        # ==========================================
        # 7. MENSAGEM DE SUCESSO E ASSINATURA
        # ==========================================
        print(f"\n[+] Estrutura criada com sucesso em: {path}")
        print("  -> .github/workflows/security-gate.yml (CI/CD Injetado)")
        print("  -> .memory/ARCHITECTURE.md (Com lista de stacks populada)")
        print("  -> .memory/STATE.md (Estado)")
        print("  -> .memory/pre-deploy-security-checklist.md (Checklist Injetado)")
        print("  -> .memory/patterns/ (Regras consolidadas injetadas)")
        print("  -> CLAUDE.md & .cursorrules (Regras do Coordenador injetadas)")
        print("\n" + "="*65)
        print("Desenvolvido com 🧠 por Matheus Valpassos*")
        print("https://github.com/matheus-valpassos")
        print("Mtech - Purr. Ecosystem")
        print("="*65)

    except Exception as e:
        print(f"\n[Erro]: {e}")

if __name__ == "__main__":
    create_memory_structure()
    input("\nPressione ENTER para fechar...")