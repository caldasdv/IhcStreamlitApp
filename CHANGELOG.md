# Changelog

## [Unreleased]

### Added

- Preparação da Sprint 0: `AGENTS.md`, documentação de inception, arquitetura, banco e ADRs.
- Template seguro de configuração do MongoDB Atlas para Streamlit Community Cloud.
- Primeiras regras de domínio de sessões extraídas e testes unitários preparados.
- Conexão, seed, repositories e services separados da UI; testes com fakes adicionados.
- Telas separadas em `app_pages/` com navegação nativa e carregamento com feedback visível.
- Edição/reagendamento, confirmação de exclusão e visão semanal adicionados.
- Dashboard de progresso com métricas semanais e gráficos nativos adicionado.
- Revisão de IHC/UX aplicada ao dashboard e aos fluxos de gravação, com estados de erro, tabela alternativa e foco visível.
- Skill repo-local de auditoria de segurança adicionada, com checklist por stack, regras de evidência e geração de relatório PDF/Markdown para issues.
- Testes de normalização, autorização de disciplina e confirmação de escritas MongoDB adicionados.
- Períodos acadêmicos adicionados com seleção do período atual, arquivamento protegido e testes de domínio/service.
- Índice documental, catálogo de domínio e workflow Git adicionados; `AGENTS.md` consolidado sem regras duplicadas.
- Disciplinas e novas sessões associadas ao período acadêmico atual, com isolamento por usuário/período e tratamento explícito dos registros legados.

### Changed

- README atualizado com instalação, configuração, testes e deploy.
- `.gitignore` reforçado para secrets, ambientes virtuais e caches de teste.
- Relatório de inspeção heurística registrado em `docs/ihc-review.md`.
- Entrypoints `app.py` e `src/app.py` consolidados no mesmo shell para reduzir divergências de deploy.
- Login Google OIDC, resolução de usuário por identidade estável e índice parcial de isolamento adicionados.
- Confirmações de ações passaram a sobreviver ao rerun e são consumidas uma única vez.
- Roadmap das Sprints 8–12 de frontend, componentes externos e avaliação de IHC documentado.
- Fundação visual da Sprint 8 aplicada com componentes reutilizáveis, tokens CSS e ajustes responsivos.
- Spike da Sprint 9 adicionado com agenda visual em Custom Component v2 e fallback textual.
- Dashboard da Sprint 10 atualizado com Plotly, filtro por disciplina e tooltips com unidades.
- Sprint 11 aplicada com filtros visíveis, datas completas, retry de carregamento e ajustes responsivos/acessíveis.
- Hardening de consultas temporais, disciplinas duplicadas, status atrasado, empty states, feedback de persistência e configuração reproduzível de testes aplicado.
- Navegação e composição de services atualizadas para o contexto de períodos acadêmicos da Sprint 14.
