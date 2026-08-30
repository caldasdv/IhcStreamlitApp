# Plano — planejador de estudos

## Objetivo

Permitir que estudantes planejem, executem e acompanhem sessões de estudo com clareza e baixo atrito.

Este repositório está na Sprint 0: a aplicação existente é um protótipo funcional e a base de arquitetura, segurança e planejamento foi documentada antes da próxima refatoração.

## Stack

Python, Streamlit, PyMongo, MongoDB Atlas e pytest. Pandas/Plotly só serão adicionados quando uma necessidade real justificar o impacto no deploy.

## Arquitetura

O alvo é um monólito modular: Presentation (Streamlit) → Services → Domain → Repositories → MongoDB Atlas. O protótipo atual ainda concentra essas responsabilidades em `src/app.py`; a extração ocorrerá por fatias na Sprint 1.

Veja [docs/architecture.md](docs/architecture.md), [docs/database.md](docs/database.md) e [docs/backlog.md](docs/backlog.md).

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

No estado atual não há testes automatizados. As regras ainda estão acopladas ao módulo Streamlit e serão extraídas antes da cobertura unitária da Sprint 1.

## Rodar em uma VPS ou no Community Cloud

Configure `MONGODB_URI` nas variáveis de ambiente ou nos Secrets do Community Cloud. O app não depende de SQLite, Google Drive ou armazenamento local persistente.

O entrypoint da raiz (`app.py`) encaminha para `src/app.py`, portanto é o entrypoint recomendado no Community Cloud. Selecione o arquivo `app.py` na raiz e confirme que `requirements.txt` está sendo lido.
