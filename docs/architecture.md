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

- **Presentation:** páginas, formulários, navegação, tabelas, gráficos, estados vazios e mensagens.
- **Application/Services:** coordenação de criação, atualização, conclusão, reagendamento e consultas de progresso.
- **Domain:** modelos de usuário, disciplina e sessão; status, prioridades, validações e conflitos de horário.
- **Infrastructure:** configuração (`st.secrets`/ambiente), conexão cacheada, índices, repositories e logging.

Na Sprint 1, as regras puras de sessão foram extraídas para `src/domain/session_rules.py` e a UI passou a utilizá-las. O restante do protótipo permanece em `src/app.py` para preservar comportamento; repositories e services serão extraídos nas próximas fatias.

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

## Riscos

- `src/app.py` ainda concentra responsabilidades e dificulta testes isolados.
- O usuário de teste e o seed automático não são autenticação nem estratégia de produção.
- A conexão MongoDB atual e o banco usado ainda precisam ser alinhados ao schema de Secrets (`mongodb.uri`/`mongodb.database`).
- Falhas de rede, limites do plano do Atlas e reruns podem causar latência ou operações repetidas.
- Não há cobertura automatizada nem validação de acessibilidade neste momento.
