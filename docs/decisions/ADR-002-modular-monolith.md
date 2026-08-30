# ADR-002 — Monólito modular

## Context

O produto é pequeno, possui uma única interface e não tem necessidade operacional de serviços distribuídos.

## Decision

Organizar Presentation, Services, Domain e Infrastructure no mesmo repositório/processo, com dependências direcionadas e repositories.

## Alternatives

Microservices, FastAPI separado, CQRS ou event-driven architecture.

## Consequences

Menor custo cognitivo e deploy simples; exige disciplina para não recolocar regras e queries dentro da UI.
