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
- Status: DONE.

### US-006

Como estudante quero uma visão semanal com ações rápidas para revisar minha carga de estudos.

- Prioridade: P1
- Critérios de aceitação: sete dias visíveis; sessões agrupadas por dia; ação de concluir disponível com feedback.
- Dependências: US-001, US-003.
- Complexidade: M
- Status: DONE.

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

**Tarefas:** agregações nativas, gráficos Streamlit somente quando responderem a uma pergunta, acessibilidade e performance.

**Riscos:** queries caras e uso excessivo de reruns.

**Definition of Done:** métricas conferidas, visualizações úteis e consultas justificadas.

### Sprint 4 — Hardening, testes e deploy

**Objetivo:** preparar operação confiável no Community Cloud.

**Histórias:** US-007, US-008 e hardening.

**Tarefas:** identidade, tratamento de erros, logging sem secrets, testes de integração controlados, revisão de requirements e checklist de deploy.

**Riscos:** configuração de Secrets, limites do Atlas/Cloud e autenticação.

**Definition of Done:** checklist de deploy aprovado, testes relevantes passam e documentação operacional atualizada.

### Sprint 4 — Revisão de IHC/UX e hardening (execução atual)

**Objetivo:** reduzir rupturas de interação e tornar falhas de leitura, consulta e gravação recuperáveis.

**Tarefas concluídas:** consistência do filtro temporal no dashboard; tabela alternativa aos gráficos;
tratamento de erros em consultas e ações; estados vazios; contraste e foco; revisão documentada em
`docs/ihc-review.md`.

**Tarefas pendentes:** definir autenticação e isolamento de dados (US-007); validar os fluxos com usuários;
revisar a dependência de seletores CSS internos após o deploy.

**Riscos:** os achados de interação ainda são inspeção estática; o comportamento real no Community Cloud
depende de configuração de Secrets, rede e latência do Atlas.

**Definition of Done:** correções testadas, falhas sem vazamento de detalhes técnicos, documentação atualizada
e limitações de avaliação registradas.

### Sprint 5 — Prontidão de deploy

**Objetivo:** garantir que os entrypoints local e Community Cloud executem exatamente a mesma aplicação.

**História:** US-009 — Como mantenedor quero um entrypoint único de aplicação para evitar divergência de comportamento no deploy.

- Prioridade: P0
- Critérios de aceitação: `app.py` e `src/app.py` usam o mesmo shell; navegação nativa é configurada uma única vez; não há caminho absoluto nem persistência local; smoke test do servidor inicia.
- Dependências: Streamlit, requirements e configuração externa de Secrets.
- Complexidade: S
- Status: DONE

**Tarefas pendentes da sprint:** checklist executado no workspace do Cloud; confirmar Secrets e rede do Atlas; definir provedor de autenticação para desbloquear US-007.

**Riscos:** a execução do Cloud pode divergir por Secrets ausentes, permissões de rede ou branch configurada.

**Definition of Done:** entrypoints convergentes, documentação atualizada, testes e smoke test passando, sem credenciais versionadas.

### Sprint 6 — Identidade e isolamento

**Objetivo:** substituir o usuário demo por identidade Google OIDC e manter os dados isolados por usuário.

**História:** US-007.

**Tarefas:** login/logout nativos; resolução por `provider + subject`; índice parcial único; remoção do seed automático;
configuração de callback local/Cloud; testes do service e validação sem credenciais no Git.

**Riscos:** redirect URI incorreto, Secrets ausentes e documentos antigos sem `identity`.

**Definition of Done:** usuário anônimo não acessa páginas; usuário autenticado é criado/recuperado por identidade;
queries usam o `user_id` resolvido; logout funciona; teste no ambiente Cloud é executado.

### Sprint 7 — Feedback confiável após rerun

**Objetivo:** manter o usuário informado quando uma ação de escrita provoca uma nova execução completa do Streamlit.

**História:** US-010 — Como estudante quero confirmar o resultado de uma ação mesmo quando a tela é recarregada.

- Prioridade: P1
- Critérios de aceitação: confirmações de criar, editar, concluir, excluir e atualizar meta aparecem após o rerun; a mensagem é exibida uma vez; falhas continuam sem expor detalhes técnicos.
- Dependências: `st.session_state` apenas para feedback transitório.
- Complexidade: S
- Status: DONE

**Definition of Done:** feedback persistido no ciclo correto, sem uso de sessão como armazenamento de dados; testes e smoke test passam.

## Definition of Ready

Objetivo, entrada, saída, critérios de aceitação, dependências e impacto arquitetural conhecidos.

## Definition of Done

Código implementado; aplicação funciona; critérios atendidos; erros tratados; testes relevantes passam; nenhuma credencial exposta; documentação atualizada; auto-review concluído.
