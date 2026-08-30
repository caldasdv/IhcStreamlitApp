# Backlog do produto

## Product Goal

Permitir que estudantes planejem, executem e acompanhem suas sessões de estudo com clareza, baixo atrito e feedback útil.

## MVP

Usuário consegue acessar seu espaço, cadastrar disciplinas, definir meta semanal, criar sessões sem conflito, visualizar agenda, concluir sessões e acompanhar progresso por disciplina, com dados persistidos no MongoDB Atlas.

## Product Backlog

### US-001

Como estudante quero visualizar minhas sessões e pendências para saber o que estudar hoje.

- Prioridade: P0
- Critérios de aceitação: agenda por dia; pendentes, concluídas e atrasadas distinguíveis; estado vazio informado.
- Dependências: acesso ao usuário e repository de sessões.
- Complexidade: M
- Status: DONE (protótipo; precisa de testes e separação arquitetural).

### US-002

Como estudante quero criar uma sessão com disciplina, assunto, objetivo, data, horário, duração e prioridade para organizar meu estudo.

- Prioridade: P0
- Critérios de aceitação: campos válidos; datas passadas rejeitadas; conflito de pendentes rejeitado; persistência confirmada.
- Dependências: subjects e validações de domínio.
- Complexidade: M
- Status: DONE (protótipo; precisa de testes e service).

### US-003

Como estudante quero concluir ou excluir uma sessão para manter meu plano atualizado.

- Prioridade: P0
- Critérios de aceitação: conclusão atualiza somente a sessão selecionada; exclusão remove somente a sessão selecionada; feedback claro.
- Dependências: repository e autorização do usuário.
- Complexidade: S
- Status: DONE (protótipo; exclusão ainda sem confirmação).

### US-004

Como estudante quero acompanhar minutos concluídos por disciplina e semana para entender meu progresso.

- Prioridade: P0
- Critérios de aceitação: minutos planejados/concluídos; meta semanal; resumo por disciplina; dados sem sessões tratados.
- Dependências: consultas e transformação de dados.
- Complexidade: M
- Status: DONE (protótipo; precisa de testes).

### US-005

Como estudante quero editar e reagendar sessões para corrigir meu plano sem recriá-las.

- Prioridade: P1
- Critérios de aceitação: edição valida os mesmos campos; reagendamento revalida conflitos; cancelamento não altera outras sessões.
- Dependências: US-002 e repositories.
- Complexidade: M
- Status: BACKLOG.

### US-006

Como estudante quero uma visão semanal com ações rápidas para revisar minha carga de estudos.

- Prioridade: P1
- Critérios de aceitação: sete dias visíveis; sessões agrupadas por dia; ação de concluir disponível com feedback.
- Dependências: US-001, US-003.
- Complexidade: M
- Status: BACKLOG.

### US-007

Como estudante quero uma identidade/autenticação real para que meus dados sejam isolados.

- Prioridade: P0
- Critérios de aceitação: usuário identificado; queries filtradas por identidade; falha de acesso tratada sem vazamento.
- Dependências: decisão de provedor e modelo de segurança.
- Complexidade: L
- Status: BLOCKED (provedor e requisito de identidade ainda não definidos).

### US-008

Como mantenedor quero testes unitários das regras fora do Streamlit para evoluir com segurança.

- Prioridade: P0
- Critérios de aceitação: validações e conflito cobertos; testes executam sem Atlas; pytest reproduzível.
- Dependências: extração de Domain/Services.
- Complexidade: M
- Status: DONE.

## Sprints

### Sprint 0 — Arquitetura e setup

**Objetivo:** registrar contexto, decisões, segurança, modelo de dados e critérios de trabalho.

**Histórias/tarefas:** setup documental, `AGENTS.md`, Secrets example, README, changelog, verificação de imports e Git.

**Riscos:** requisitos de identidade ainda incompletos.

**Definition of Done:** documentação consistente, secrets protegidos, validações executadas e nenhuma feature grande iniciada.

### Sprint 1 — Fluxo principal

**Objetivo:** extrair Domain/Services/Repositories e consolidar criar, listar, concluir e excluir sessões.

**Histórias:** US-001, US-002, US-003, US-008.

**Tarefas:** contratos de repository; modelos/validações; conexão e índices; services; testes unitários; páginas finas com `st.navigation`.

**Riscos:** compatibilidade com documentos existentes e seed.

**Definition of Done:** fluxo MVP testado sem Streamlit nas regras e funcionando no Atlas.

### Sprint 2 — Funcionalidades complementares

**Objetivo:** tornar o planejamento corrigível e mais completo.

**Histórias:** US-005, US-006.

**Tarefas:** edição/reagendamento, confirmação de exclusão, visão semanal e estados vazios.

**Riscos:** conflitos de horário em atualizações.

**Definition of Done:** critérios das histórias, testes e documentação atendidos.

### Sprint 3 — Dashboard e análises

**Objetivo:** melhorar o entendimento do progresso sem sobrecarregar a interface.

**Histórias:** US-004 e melhorias de UX/visualização.

**Tarefas:** agregações, gráficos Plotly somente se trouxerem benefício real, acessibilidade e performance.

**Riscos:** queries caras e uso excessivo de reruns.

**Definition of Done:** métricas conferidas, visualizações úteis e consultas justificadas.

### Sprint 4 — Hardening, testes e deploy

**Objetivo:** preparar operação confiável no Community Cloud.

**Histórias:** US-007, US-008 e hardening.

**Tarefas:** identidade, tratamento de erros, logging sem secrets, testes de integração controlados, revisão de requirements e checklist de deploy.

**Riscos:** configuração de Secrets, limites do Atlas/Cloud e autenticação.

**Definition of Done:** checklist de deploy aprovado, testes relevantes passam e documentação operacional atualizada.

## Definition of Ready

Objetivo, entrada, saída, critérios de aceitação, dependências e impacto arquitetural conhecidos.

## Definition of Done

Código implementado; aplicação funciona; critérios atendidos; erros tratados; testes relevantes passam; nenhuma credencial exposta; documentação atualizada; auto-review concluído.
