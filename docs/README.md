# Documentação do projeto

Este diretório concentra as fontes de verdade do Plano. Documentos históricos continuam úteis como evidência, mas não devem contradizer código, testes, backlog ou decisões vigentes.

## Estado atual

- MVP operacional: autenticação Google OIDC, isolamento por usuário, disciplinas, sessões de estudo, agenda semanal, progresso e meta semanal.
- Sprint 13: hardening concluído e incorporado à `main` pelo PR #20.
- Sprint 14: períodos acadêmicos integrados à `main` pelo PR #21.
- Sprint 15: associação de disciplinas ao período atual integrada à `main` pela PR #22.
- Sprint 16: grade semanal de aulas integrada à `main` pela PR #23.
- Sprint 17: associação manual de disciplinas legadas em desenvolvimento.
- Sprint 12: protocolo de avaliação preparado, ainda pendente de participantes e evidência real.
- Próxima decisão: integração da grade com o planejamento de sessões e política para mover disciplinas já associadas.

## Fontes de verdade

| Documento | Responsabilidade |
|---|---|
| [architecture.md](architecture.md) | arquitetura, dependências, fluxo e riscos |
| [domain.md](domain.md) | conceitos, entidades, estados e invariantes |
| [database.md](database.md) | collections, campos, índices e padrões de acesso |
| [backlog.md](backlog.md) | Product Goal, histórias, prioridades e sprints |
| [frontend-roadmap.md](frontend-roadmap.md) | decisões e evolução de frontend/IHC |
| [usability-test-plan.md](usability-test-plan.md) | protocolo ainda não executado de avaliação com usuários |
| [ihc-review.md](ihc-review.md) | inspeção estática de IHC já realizada e suas limitações |
| [git-workflow.md](git-workflow.md) | branches, commits, PRs e estratégia de integração |
| [decisions/](decisions/) | ADRs de decisões arquiteturais duráveis |

## Regras de manutenção

1. Mudança de comportamento atualiza código, testes, backlog e documentação afetada no mesmo trabalho.
2. Collection nova deve ser documentada em `database.md` antes do deploy.
3. Entidade planejada fica em `domain.md`; só entra em `database.md` quando aprovada para implementação.
4. Status de histórias usa apenas `BACKLOG`, `TODO`, `IN PROGRESS`, `BLOCKED`, `REVIEW` ou `DONE`.
5. Avaliação estática, smoke test, teste no Cloud e teste com usuários são evidências diferentes e devem ser nomeados corretamente.
6. `README.md` da raiz permanece curto e aponta para este índice.
