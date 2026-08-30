# Plano — planejador de estudos

## Objetivo

Permitir que estudantes planejem, executem e acompanhem sessões de estudo com clareza e baixo atrito.

Este repositório está na Sprint 0: a aplicação existente é um protótipo funcional e a base de arquitetura, segurança e planejamento foi documentada antes da próxima refatoração.

## Stack

Python, Streamlit, PyMongo, MongoDB Atlas e pytest. Pandas/Plotly só serão adicionados quando uma necessidade real justificar o impacto no deploy.

## Arquitetura

O projeto usa um monólito modular: Presentation (Streamlit) → Services → Domain → Repositories → MongoDB Atlas. A primeira extração foi concluída na Sprint 1; a UI agora usa services, a conexão/seed ficam em `src/database` e os adapters MongoDB em `src/repositories`.

Veja [docs/architecture.md](docs/architecture.md), [docs/database.md](docs/database.md) e [docs/backlog.md](docs/backlog.md).

## Estrutura

- `app.py`: shell, configuração visual e navegação nativa com `st.navigation`.
- `app_pages/`: uma página Streamlit por fluxo da aplicação, incluindo a visão semanal.
- `src/ui/`: contexto, sidebar, estilos e componentes reutilizáveis.
- `src/services/`: casos de uso sem dependência direta da UI.
- `src/repositories/`: contratos e adapters MongoDB.
- `src/domain/`: regras testáveis sem Streamlit.
- `tests/`: testes unitários de domínio e services.
- A tela `Progresso` inclui métricas semanais e visualizações nativas por disciplina e por dia.

## Regras atuais

- sessões só podem ser planejadas para hoje ou uma data futura;
- sessões pendentes com data passada aparecem como atrasadas;
- horários de sessões pendentes não podem se sobrepor;
- a visão geral acompanha a meta semanal em horas;
- a página de progresso resume o tempo concluído por disciplina;
- a conexão usa `MONGODB_URI` e o banco `plano_estudos` no Atlas.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Para desenvolvimento e testes, instale também `requirements-dev.txt`.

## Configuração local e Secrets

As credenciais locais ficam em `.env`, que não é versionado, com:

```dotenv
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER/
```

No Streamlit Community Cloud, configure o Secret `MONGODB_URI` ou use o formato documentado em [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example). Nunca commite `.env` ou `.streamlit/secrets.toml`.

O banco padrão do protótipo é `plano_estudos`; a configuração de nome de banco será consolidada junto com a conexão na Sprint 1.

## Execução e testes

```bash
streamlit run app.py
pytest -q
```

As primeiras regras de domínio já possuem testes em `tests/unit`; execute pytest após instalar `requirements-dev.txt`.

## Rodar em uma VPS ou no Community Cloud

Configure `MONGODB_URI` nas variáveis de ambiente ou nos Secrets do Community Cloud. O app não depende de SQLite, Google Drive ou armazenamento local persistente.

O entrypoint da raiz (`app.py`) encaminha para `src/app.py`, portanto é o entrypoint recomendado no Community Cloud. Selecione o arquivo `app.py` na raiz e confirme que `requirements.txt` está sendo lido.
