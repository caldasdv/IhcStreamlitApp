# ADR-003 — Streamlit Community Cloud

## Context

O produto é uma aplicação Streamlit e o Community Cloud é um alvo de deploy explícito, com execução efêmera e configuração por Secrets.

## Decision

Manter `app.py` na raiz, dependências em `requirements.txt`, configuração em `st.secrets` e persistência somente no MongoDB Atlas.

## Alternatives

VPS ou plataforma web genérica; podem ser considerados depois, mas aumentam operação e não são necessários para o MVP.

## Consequences

O app deve tolerar reruns, não depender de disco local, manter dependências compatíveis e nunca versionar secrets. A conexão deve usar `st.cache_resource`.
