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

### Changed

- README atualizado com instalação, configuração, testes e deploy.
- `.gitignore` reforçado para secrets, ambientes virtuais e caches de teste.
- Relatório de inspeção heurística registrado em `docs/ihc-review.md`.
- Entrypoints `app.py` e `src/app.py` consolidados no mesmo shell para reduzir divergências de deploy.
- Login Google OIDC, resolução de usuário por identidade estável e índice parcial de isolamento adicionados.
- Confirmações de ações passaram a sobreviver ao rerun e são consumidas uma única vez.
- Roadmap das Sprints 8–12 de frontend, componentes externos e avaliação de IHC documentado.
