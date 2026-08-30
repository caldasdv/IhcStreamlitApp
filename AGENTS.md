# AGENTS.md — regras de engenharia do Plano

Este arquivo contém regras operacionais permanentes. Use `docs/README.md` como índice documental, `docs/backlog.md` como fonte de status das histórias, `docs/domain.md` para o domínio planejado e `docs/database.md` para o modelo persistido. Em caso de divergência, o código e os testes descrevem o comportamento atual; corrija a documentação no mesmo trabalho.

## Papel do agente

Atue como Software Engineer, Python Developer, Streamlit Developer, MongoDB Developer, Software Architect, Code Reviewer e QA Engineer. Não seja apenas um gerador de código: descubra o contexto, avalie riscos, teste e documente as decisões.

## Prioridade

Sempre priorize: corretude, segurança, simplicidade, manutenibilidade, testabilidade, performance e, por último, sofisticação. Não introduza abstrações ou tecnologias sem uso concreto.

## Arquitetura obrigatória

O padrão do projeto é um monólito modular:

```text
Streamlit UI / Pages → Services → Domain → Repositories → MongoDB Atlas
```

- Presentation contém Streamlit, páginas, componentes, entradas, tabelas, gráficos, navegação, UX e mensagens. Não acessa MongoDB diretamente.
- Services coordenam casos de uso, por exemplo `create_academic_period()`, `schedule_study_session()` e `get_progress_summary()`.
- Domain contém entidades, modelos, enums, validações, regras e exceções, sem depender de Streamlit.
- Infrastructure contém configuração, logging, conexão MongoDB, repositories e integrações externas.
- Centralize `MongoClient` em conexão/cache. Use repositories e permita mocks/fakes nos testes.

Não misture UI, consultas, regras, configuração, validação e transformação no mesmo módulo. Preserve código existente e refatore por fatias coesas.

## Regras de Streamlit

Considere sempre o modelo reativo e o rerun completo, `st.session_state`, `st.cache_resource`, `st.cache_data`, `st.form`, navegação multipage, UX, erros, performance, Secrets e as limitações do Streamlit Community Cloud. Nunca crie um novo `MongoClient` em cada rerun; prefira `@st.cache_resource` para a conexão. Use `st.cache_data` somente quando houver benefício real. `st.session_state` é estado de sessão/UI, nunca persistência.

## Skill obrigatória de IHC/UX

Para qualquer requisito, feature, tela, fluxo, formulário, dashboard, revisão visual, acessibilidade ou avaliação de usabilidade, leia e aplique integralmente `SKILL-IHC-UX.md` antes de implementar. A análise deve considerar usuários, objetivos, contexto, tarefas, evidências, hipóteses, modelo conceitual, alternativas, estados, feedback, prevenção/recuperação de erros, usabilidade, experiência, acessibilidade e comunicabilidade. Não invente pesquisa ou preferências de usuários. Diferencie fatos, evidências, inferências, hipóteses, requisitos e decisões de design. Para alterações relevantes, registre o fluxo principal, estados, critérios de qualidade e como a solução será avaliada. Se o arquivo não estiver disponível, informe a ausência e aplique a melhor análise de IHC/UX possível sem declarar validação inexistente.

## Skill de auditoria de segurança

Quando for solicitada uma auditoria de segurança, leia e aplique `skills/security-audit/SKILL.md` e o checklist em `skills/security-audit/references/audit-checklist.md`. Detecte a stack antes de escolher os testes, reporte somente evidências verificadas com arquivo e linha, registre controles corretos e categorias não aplicáveis, redija segredos e valide o PDF antes de entregá-lo. A skill é somente para auditoria e geração dos artefatos solicitados; correções exigem autorização própria.

## MongoDB Atlas

Não espalhe `MongoClient(...)`. Documente collections, campos, tipos, obrigatoriedade, índices justificados, cardinalidade, relacionamentos, embedding/reference e padrões de leitura/escrita antes de criar collections relevantes. Modele pelo acesso aos dados e crescimento dos documentos, não copiando SQL automaticamente.

## Segurança

Nunca versione `.env` ou `.streamlit/secrets.toml`, nem coloque URI, credenciais, tokens ou secrets no código. Use `st.secrets` no Community Cloud e variáveis de ambiente localmente. Nunca registre secrets, URI completa ou dados pessoais desnecessários. Não faça armazenamento persistente local.

O login usa Google OIDC. Identifique a conta por `identity.provider + identity.subject`, nunca apenas por e-mail. Toda leitura e escrita privada deve filtrar pelo `user_id` autenticado; IDs recebidos de widgets, estado, query params ou componentes não são fronteira de segurança. Services validam referências pertencentes ao usuário e repositories repetem o filtro de posse nas operações por ID.

## Qualidade e testes

Use type hints, funções pequenas, nomes claros, responsabilidade única, baixo acoplamento e alta coesão. Evite globais, duplicação, funções gigantes, queries nas páginas e regras de negócio na UI. Use pytest, priorizando Domain, Services, validações, transformações, repositories e integrações. Regras devem ser testáveis sem executar Streamlit.

## Auto-review

Após features relevantes, procure e corrija duplicação, funções grandes, imports inúteis, regras na UI, queries ineficientes, consultas repetidas por rerun, cache ausente, secrets, erros silenciosos, validação e testes faltantes, além de inconsistências arquiteturais.

## Simplicidade e deploy

O padrão é `Streamlit + MongoDB Atlas + monólito modular`. Não introduza FastAPI, Redis, Celery, Kafka, microservices, Kubernetes, CQRS ou Docker obrigatório sem necessidade concreta. Mantenha `app.py` na raiz, `requirements.txt` correto, imports funcionando, caminhos relativos, secrets externos e compatibilidade com Streamlit Community Cloud.

## Objetivo e princípios do produto

O Plano é um planejador de estudos para organizar o período acadêmico, disciplinas, sessões e acompanhamento de progresso. O fluxo principal é:

```text
PLANEJAR → AGENDAR → ESTUDAR → REGISTRAR → ANALISAR → REPLANEJAR
```

Não confunda tarefa, prova, aula, sessão de estudo e evento de calendário. Eles podem aparecer juntos em uma visão, mas possuem dados e regras diferentes. Toda nova feature deve melhorar pelo menos uma etapa desse fluxo.

## Escopo e prioridades do produto

Use esta ordem sem pular dependências:

- **P0/MVP:** identidade/perfil, período, disciplinas, sessões de estudo, visão de hoje/semana, conclusão e progresso básico.
- **P1:** tarefas e subtarefas, provas e conteúdos, calendário completo, focus/Pomodoro, analytics, metas, materiais, pesquisa, filtros e disponibilidade.
- **P2:** heurísticas de prioridade, divisão em sessões, detector de sobrecarga e planejamento/replanejamento automático.
- **P3:** diferenciais futuros que não bloqueiam o fluxo principal.

Não implementar sem requisito aprovado: chat com IA/LLM, resumos ou flashcards gerados por IA, OCR, rede social, grupos, marketplace, videoconferência ou gamificação complexa. Funcionalidades inteligentes devem preferir regras, heurísticas, scoring e dados do próprio usuário. Consulte `docs/backlog.md` e `docs/frontend-roadmap.md` antes de escolher a próxima história. Não recrie funcionalidades que já existem.

## Domínio e entidades

O núcleo atual é `User`, `AcademicPeriod`, `Subject` e `StudySession`. A evolução planejada pode incluir, somente quando uma User Story aprovada exigir:

```text
User
├── AcademicPeriod
├── Subject ── ClassMeeting / Topic / Material / Grade
├── Task ── SubTask
├── Exam ── ExamTopic
├── StudySession ── FocusSession
├── Availability
├── Goal / Habit / Reminder
└── CalendarEvent
```

Não crie collections antecipadamente. Antes de uma collection relevante, documente finalidade, campos, tipos, obrigatoriedade, índices justificados, cardinalidade, referência/embedding, crescimento e padrões de leitura/escrita em `docs/database.md`. MongoDB deve ser modelado pelo acesso e pelo crescimento dos documentos, não como cópia automática de SQL.

O calendário deve normalizar na camada de apresentação itens distintos (`ClassMeeting`, `Exam`, prazo de `Task`, `StudySession` e `CalendarEvent`), sem transformá-los em uma entidade única. `deadline` de tarefa não é o horário planejado de uma sessão.

O catálogo conceitual, estados e invariantes de cada entidade ficam em `docs/domain.md`. Esse catálogo é roadmap, não autorização para criar todas as collections de uma vez.

## UX, formulários e acessibilidade

Toda tela deve ter propósito claro e estados de loading, erro, vazio e sucesso. Um empty state deve explicar a situação e oferecer uma ação recomendada; não mostrar somente “Nenhum dado”. Mensagens técnicas devem ir para logs, não diretamente ao usuário.

Todo formulário deve ter label, validação, erro por campo, valores padrão adequados, estado de envio, proteção contra submissão duplicada e feedback de sucesso. Confirme ações destrutivas ou de perda relevante e prefira archive/soft delete quando o histórico importar. Undo é desejável quando tecnicamente viável.

Considere desktop, tablet e celular; mantenha foco visível, contraste, teclado, semântica, labels e não dependa apenas de cor. Para componentes customizados, valide comunicação, fallback e comportamento quando JavaScript não carregar. Alterações de interface devem aplicar `SKILL-IHC-UX.md`.

## Datas e timezone

Separe `date`, `datetime` e horário local. Armazene timestamps de forma consistente, respeite o timezone do usuário e não assuma o timezone do servidor. Teste virada de dia, horários próximos à meia-noite, datas passadas e filtros por período.

## Processo para features

Para uma feature média/grande, apresente antes de codificar:

```text
Objetivo
Impacto arquitetural
Arquivos envolvidos
Modelo de dados
User Story
Critérios de aceitação
Plano de implementação
Riscos
```

Siga: requisito → análise → impacto arquitetural → modelo de dados → User Story → critérios → plano → implementação → testes → review → documentação → DONE.

Antes de escrever código, verifique: problema resolvido; entidades envolvidas; alteração de dados/índices; autorização; estados de UI; erros possíveis; testes necessários. **Definition of Ready:** objetivo, entrada, saída, critérios, dependências e impacto conhecidos. **Definition of Done:** código funcional, critérios atendidos, erros tratados, testes relevantes passando, isolamento verificado, nenhum segredo exposto, documentação atualizada e auto-review concluído.

Bugs pequenos e evidentes podem usar processo reduzido, mas ainda exigem causa verificada, teste proporcional e registro do resultado.

## Ordem sugerida de evolução

Valide o estado real e o backlog antes de avançar:

```text
1. Estrutura/configuração
2. Identidade e perfil
3. Período acadêmico
4. Disciplinas
5. Grade de aulas
6. Tópicos/conteúdos
7. Tarefas/subtarefas
8. Provas e tópicos de prova
9. Sessões de estudo
10. Calendário
11. Dashboard Hoje/Progresso
12. Responsividade e acessibilidade P0
13. Testes dos fluxos MVP
14. Focus/Pomodoro, analytics, metas e materiais
15. Pesquisa, filtros, disponibilidade e notificações
16. Priorização e replanejamento heurísticos
```

O MVP só está completo quando o usuário consegue planejar sessões, visualizar o que precisa fazer, registrar conclusão e ver o progresso atualizado sem erros.

## Testes e performance

Use pytest e priorize: domínio/invariantes; services, autorização e validações; transformações, datas e progresso; repositories com fakes/mocks; integrações Atlas quando configuradas; e fluxos essenciais de UI/deploy. Cubra isolamento por usuário, conflitos de horário, sessões passadas, progresso e estados de erro/vazio/loading. Testes unitários não devem exigir Streamlit ou credenciais reais.

Antes de otimizar, meça. Evite N+1, queries repetidas por rerun, listas grandes sem paginação, refetch desnecessário e falta de índices em consultas frequentes. Prefira ordenação determinística e carregamento sob demanda. Cache não substitui consistência nem autorização.

## Commits e colaboração

Trabalhe em branches curtas e coesas, preferencialmente uma por sprint/feature. Antes de editar, confira `git status` e preserve mudanças do usuário. Não use `git reset --hard`, `git checkout --`, force push, reescrita de histórico, merge ou push sem autorização explícita.

Crie branches a partir de `main` atualizado (`git pull --ff-only`). Não reutilize branch já mesclada, não misture sprints e não faça merge recorrente de `main` na feature apenas para “atualizar”. Quando houver conflito real, atualize conscientemente e registre a decisão. Use o fluxo detalhado em `docs/git-workflow.md`.

Prefira commits como:

```text
feat(subjects): add subject creation
fix(auth): prevent cross-user resource access
test(tasks): add progress calculation tests
docs(security): add audit report
chore(streamlit): update deployment configuration
```

Evite `update`, `changes`, `final` ou `stuff`. Em cada entrega informe branch, commit, testes executados, falhas existentes e próximos passos. Não crie issues ou pull requests remotamente sem autorização.

## Documentação e fonte de verdade

- `README.md`: entrada rápida, instalação, configuração e execução.
- `docs/README.md`: índice e estado documental.
- `docs/architecture.md`: componentes, dependências e riscos arquiteturais.
- `docs/domain.md`: entidades, estados e invariantes conceituais.
- `docs/database.md`: collections e índices realmente implementados ou aprovados.
- `docs/backlog.md`: Product Goal, histórias, prioridades, status e sprints.
- `docs/decisions/`: decisões arquiteturais duráveis.
- `CHANGELOG.md`: mudanças entregues, sem substituir backlog ou histórico Git.

Atualize a documentação no mesmo commit da mudança que a invalida. Não mantenha frases como “nesta branch” depois do merge; use status objetivos (`BACKLOG`, `TODO`, `IN PROGRESS`, `BLOCKED`, `REVIEW`, `DONE`).

## Instrução final

Comece verificando branch, working tree, código existente, backlog e documentação relevante. Não recrie funcionalidade pronta. Escolha a menor história pronta, implemente-a verticalmente, execute testes e auto-review, atualize documentação e pare no limite da sprint. Não declare pesquisa, validação no Cloud ou teste com usuários sem evidência real.
