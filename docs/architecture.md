# Arquitetura

## Visão geral

O Plano é um planejador de estudos web para estudantes. O MVP Streamlit possui autenticação Google OIDC, períodos acadêmicos, disciplinas, grade de aulas, sessões, meta semanal, agenda e visão de progresso, com isolamento por usuário. A arquitetura é um monólito modular adequado ao tamanho atual e ao deploy no Streamlit Community Cloud.

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

As regras puras ficam em `src/domain`, a UI depende de services e as telas são scripts em `app_pages/` usando `st.navigation`. O shell compartilhado em `src/ui/app_shell.py` garante o mesmo comportamento quando o Community Cloud ou uma configuração local usa `app.py` ou `src/app.py`. Conexão e índices estão em `src/database`; adapters MongoDB ficam em `src/repositories`. Consultas de agenda/progresso recebem intervalos de data, e services validam posse do usuário e vínculo da disciplina ao período atual antes de persistir sessões.

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
- O período acadêmico atual é uma referência no usuário; períodos possuem repository/service próprios e não são embutidos nem inferidos a partir de datas.
- Disciplinas novas referenciam um período ativo. Registros legados sem período são preservados e apresentados explicitamente, sem migração automática.

## Riscos

- Documentos legados sem identidade não são associados automaticamente a uma conta autenticada; o seed demonstrativo não é executado pelo container da aplicação.
- Documentos legados de disciplina ainda podem não possuir `name_normalized`; o service cobre duplicidade, mas uma migração controlada continua pendente.
- Disciplinas ainda não estão vinculadas a períodos; essa associação requer fluxo explícito e tratamento dos dados legados.
- A configuração aceita o schema de Secrets (`mongodb.uri`/`mongodb.database`) e mantém fallback local por ambiente.
- Falhas de rede, limites do plano do Atlas e reruns podem causar latência ou operações repetidas.
- Há testes unitários, mas ainda faltam testes automatizados de UI, integração Atlas e validação de acessibilidade em navegador real.
