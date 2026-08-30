# Plano — planejador de estudos

## Objetivo

Permitir que estudantes planejem, executem e acompanhem sessões de estudo com clareza e baixo atrito.

O MVP funcional já passou pelas Sprints 0–11; a Sprint 12 possui plano de avaliação com usuários e o hardening técnico atual reforça consistência, isolamento e operação no Community Cloud.

## Stack

Python, Streamlit, Authlib, PyMongo, Plotly, MongoDB Atlas e pytest. Pandas só será adicionada quando uma necessidade real justificar o impacto no deploy.

## Arquitetura

O projeto usa um monólito modular: Presentation (Streamlit) → Services → Domain → Repositories → MongoDB Atlas. A primeira extração foi concluída na Sprint 1; a UI agora usa services, a conexão/seed ficam em `src/database` e os adapters MongoDB em `src/repositories`.

Veja [docs/architecture.md](docs/architecture.md), [docs/database.md](docs/database.md) e [docs/backlog.md](docs/backlog.md).

Para auditorias de segurança, use a skill repo-local em [`skills/security-audit/SKILL.md`](skills/security-audit/SKILL.md). Ela define a descoberta da stack, a matriz de evidências e a geração validada do relatório PDF.

O roadmap de evolução visual e componentes externos está em [docs/frontend-roadmap.md](docs/frontend-roadmap.md).

## Estrutura

- `app.py`: shell, configuração visual e navegação nativa com `st.navigation`.
- `app_pages/`: uma página Streamlit por fluxo da aplicação, incluindo visão semanal e períodos acadêmicos.
- `src/ui/`: contexto, sidebar, estilos e componentes reutilizáveis.
- `src/services/`: casos de uso sem dependência direta da UI.
- `src/repositories/`: contratos e adapters MongoDB.
- `src/domain/`: regras testáveis sem Streamlit.
- `tests/`: testes unitários de domínio e services.
- A tela `Progresso` inclui métricas semanais e visualizações Plotly por disciplina e por dia, com tabela textual equivalente.

## Regras atuais

- sessões só podem ser planejadas para hoje ou uma data futura;
- sessões pendentes com data passada aparecem como atrasadas;
- horários de sessões pendentes não podem se sobrepor;
- a visão geral acompanha a meta semanal em horas;
- a página de progresso resume o tempo concluído por disciplina;
- a conexão usa `MONGODB_URI` e o banco `plano_estudos` no Atlas.
- o primeiro período acadêmico criado vira o atual; períodos não atuais podem ser arquivados sem apagar o histórico.

## Rodar localmente

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Para desenvolvimento e testes, instale também `requirements-dev.txt`.

## Configuração local e Secrets

As credenciais locais ficam em `.env`, que não é versionado, com:

```dotenv
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER/
```

No Streamlit Community Cloud, configure o Secret `MONGODB_URI` ou use o formato documentado em [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example). Nunca commite `.env` ou `.streamlit/secrets.toml`.

Para autenticação local, crie um cliente OIDC no Google Cloud e registre
`http://localhost:8501/oauth2callback` como redirect URI. No Community Cloud, troque o redirect
URI pela URL publicada terminada em `/oauth2callback` e cole o bloco `[auth]` nos Secrets. O
usuário é associado ao `sub` estável do Google; o e-mail não é usado como chave de isolamento.

O banco padrão é `plano_estudos`, mas o nome pode ser definido no Secret `[mongodb].database` ou
em `MONGODB_DATABASE` no ambiente local.

## Execução e testes

```bash
python -m streamlit run app.py
python -m pytest -q
```

As regras de domínio, services, transformações, gráficos e resultados de escrita dos repositories possuem testes em `tests/unit`; execute pytest após instalar `requirements-dev.txt`. O projeto suporta Python 3.11 a 3.14, conforme `pyproject.toml`.

## Rodar em uma VPS ou no Community Cloud

Configure `MONGODB_URI` nas variáveis de ambiente ou nos Secrets do Community Cloud. O app não depende de SQLite, Google Drive ou armazenamento local persistente.

O entrypoint recomendado no Community Cloud é `app.py` na raiz. `src/app.py` mantém compatibilidade com configurações antigas e usa o mesmo shell de navegação; ambos carregam `requirements.txt` e não armazenam dados localmente.
