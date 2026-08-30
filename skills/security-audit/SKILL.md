---
name: security-audit
description: Audita a segurança de um repositório pela stack detectada, reporta somente evidências verificadas e gera um relatório PDF pt-BR com issues prontas para o GitHub.
---

# Skill de auditoria de segurança

Use esta skill quando o usuário pedir uma auditoria de segurança do projeto, revisão de vulnerabilidades ou relatório de segurança. A auditoria é baseada no código real e deve ser adaptada à stack detectada antes de classificar qualquer categoria.

## Princípios obrigatórios

- Leia o repositório e detecte linguagem, framework, persistência/ORM ou query builder, autenticação/autorização, frontend e arquivos de deploy antes de auditar.
- Reporte somente achados verificados. Não transforme ausência de evidência em vulnerabilidade e não declare segurança global; delimite o escopo revisado.
- Percorra todos os handlers/rotas e pontos equivalentes da stack, não uma amostra.
- Para cada achado registre arquivo, linha exata, trecho mínimo, condição de explorabilidade, explicação e severidade.
- Registre também os controles verificados e corretos. Diga explicitamente quando uma categoria não se aplica.
- Não exponha segredos descobertos no chat, no PDF, nos logs ou em novos arquivos; redija valores sensíveis e recomende rotação quando necessário.
- A auditoria não autoriza corrigir o produto nem criar issues remotamente. Gere apenas o relatório e artefatos locais pedidos.

## Procedimento

1. Faça o inventário da stack e do escopo. Preserve o estado do repositório; não faça alterações destrutivas nem reescreva histórico.
2. Execute a matriz de verificação em `references/audit-checklist.md`, mapeando cada categoria para os mecanismos encontrados.
3. Compile uma matriz de evidências com achados, pontos fortes, categorias não aplicáveis, condições de exploração e cobertura revisada.
4. Gere o relatório em `docs/security-audit/relatorio-auditoria-seguranca.pdf` e deixe o gerador reproduzível em `docs/security-audit/generate_report.py` (ou nome equivalente documentado).
5. Valide o PDF: páginas A4, gráficos renderizados, tabelas legíveis, cabeçalho/rodapé e ausência de segredos. Use uma venv local ou temporária; nunca instale globalmente.
6. Entregue no chat o inventário, os achados arquivo a arquivo/linha a linha, pontos fortes, categorias não aplicáveis, limitações e todos os caminhos gerados.

## Artefatos mínimos

O PDF deve estar em pt-BR e conter capa, data, escopo e nota metodológica; resumo executivo com contagens, rosca por severidade e barras por categoria; pontos fortes e fracos; tabela detalhada; recomendações P1/P2/P3; e a seção final `ISSUES PARA O GITHUB` com blocos Markdown completos e copiáveis para cada achado acionável. Use as cores `#B91C1C` (crítica), `#EA580C` (alta), `#D97706` (média), `#2563EB` (baixa) e `#059669` (ponto forte).

Se bibliotecas de PDF/gráficos não estiverem disponíveis, crie uma venv sob `.venv/` ou `/tmp`, instale somente o necessário nela e registre as limitações. Não adicione dependências permanentes ao produto sem justificar impacto no deploy.

Consulte o checklist para os critérios completos, o formato das evidências, o modelo de severidade e o template de issues.
