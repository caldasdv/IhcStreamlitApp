# ADR-004 — Custom Component v2 para agenda visual

## Context

A visão semanal precisava de uma representação mais rápida para localizar sessões, mas a interface
não deve misturar regras de negócio, queries ou um frontend independente. Os widgets nativos
continuam adequados para formulários e ações transacionais.

## Decision

Implementar um spike inline com Custom Component v2 do Streamlit. O componente recebe somente dados
serializáveis preparados pela página e emite o identificador da sessão selecionada. A lista nativa
por dia permanece como fallback e alternativa textual. O componente usa tokens de tema do Streamlit,
foco visível e construção DOM com `textContent` para não injetar dados do usuário.

## Alternatives

- Manter somente a lista nativa: menor risco, mas não atende tão bem à localização espacial na semana.
- Adicionar biblioteca de calendário de terceiros: interação potencialmente mais rica, porém adiciona dependência, risco de acessibilidade e custo de deploy antes de validar a necessidade.
- Reescrever a interface em React: desproporcional ao monólito atual e incompatível com a política de simplicidade.

## Consequences

Há um pequeno bloco de JavaScript confiável dentro da camada de apresentação e o requisito mínimo
do Streamlit sobe para uma versão que suporta Custom Components v2. A interação é experimental e
precisa de teste no Community Cloud e com usuários antes de virar componente de produção. Falha de
renderização não impede a consulta da lista textual.
