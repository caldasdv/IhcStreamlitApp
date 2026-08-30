# ADR-001 — MongoDB Atlas

## Context

O produto precisa de persistência externa compatível com Streamlit Community Cloud e com crescimento simples de sessões, disciplinas e usuários.

## Decision

Usar MongoDB Atlas via PyMongo, com conexão centralizada/cacheada, repositories e índices documentados.

## Alternatives

SQLite/local files (não adequados para persistência compartilhada no Cloud), PostgreSQL (mais estrutura relacional que o MVP exige), outro serviço gerenciado (sem requisito atual).

## Consequences

Há dependência de rede e configuração segura de Secrets, mas os dados persistem fora do processo e o modelo é adequado a consultas por usuário e agenda.
