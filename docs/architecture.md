# Arquitetura

## Visão geral

O Plano é um planejador de estudos web para estudantes. O estado atual é um protótipo Streamlit funcional com usuário de teste, disciplinas, sessões, meta semanal e visão de progresso. A direção arquitetural é um monólito modular, adequado ao tamanho atual e ao deploy no Streamlit Community Cloud.

## Componentes

```text
app.py / pages
        ↓
UI e componentes Streamlit
        ↓
Services / casos de uso
        ↓
Domain / modelos e regras
        ↓
Repositories
        ↓
Database connection / MongoDB Atlas
```

- **Presentation:** `app.py`, `src/ui/app_shell.py`, `app_pages/` e os demais módulos de `src/ui/` contêm shell, páginas, formulários, navegação, tabelas, gráficos, estados vazios e mensagens.
- **Application/Services:** coordenação de criação, atualização, conclusão, reagendamento e consultas de progresso.
- **Domain:** modelos de usuário, disciplina e sessão; status, prioridades, validações e conflitos de horário.
- **Infrastructure:** configuração (`st.secrets`/ambiente), conexão cacheada, índices, repositories e logging.

Na Sprint 1, as regras puras de sessão foram extraídas para `src/domain/session_rules.py`, a UI passou a depender de services e as telas foram separadas em `app_pages/` usando `st.navigation`. O shell compartilhado em `src/ui/app_shell.py` garante o mesmo comportamento quando o Community Cloud ou uma configuração local usa `app.py` ou `src/app.py`. Conexão, índices e seed estão em `src/database`; adapters MongoDB estão em `src/repositories`. O carregamento de cada tela mostra spinner e erro visível, sem bloquear a navegação antes de selecionar uma página.

## Responsabilidades e dependências

Presentation pode depender de Services e modelos de saída. Services podem depender de Domain e interfaces de repository. Implementações MongoDB ficam atrás dessas interfaces. Domain não depende de Streamlit, PyMongo ou variáveis de ambiente.

## Fluxo de dados

1. Streamlit renderiza uma página e coleta entradas, preferencialmente em `st.form`.
2. Um service valida/coordenada a operação.
3. O repository traduz a operação para uma query MongoDB.
4. O service devolve modelos/DTOs; a UI transforma dados para tabelas ou gráficos.
5. A conexão é criada uma vez por processo via `st.cache_resource`; não há persistência local.

## Decisões

- Monólito modular, sem serviços distribuídos nesta fase.
- MongoDB Atlas como persistência externa.
- Streamlit como presentation e Community Cloud como alvo de deploy.
- Segredos fora do Git; `st.secrets` no Cloud e ambiente local para desenvolvimento.
- O shell exige autenticação OIDC antes da navegação; o service resolve o usuário por `identity.provider` e `identity.subject`, e os repositories continuam filtrando por `user_id`.

## Riscos

- `src/app.py` ainda concentra responsabilidades e dificulta testes isolados.
- Documentos legados sem identidade não são associados automaticamente a uma conta autenticada; o seed demonstrativo não é executado pelo container da aplicação.
- A configuração aceita o schema de Secrets (`mongodb.uri`/`mongodb.database`) e mantém fallback local por ambiente.
- Falhas de rede, limites do plano do Atlas e reruns podem causar latência ou operações repetidas.
- Não há cobertura automatizada nem validação de acessibilidade neste momento.
