# Workflow Git e revisão do histórico

## Estado observado

O histórico preserva todas as entregas e PRs. As branches temporárias antigas foram removidas após a integração;
`main` é a única branch persistente do projeto.

Decisão: preservar o histórico existente e consolidar o trabalho na `main`.

## Fluxo obrigatório

### 1. Atualizar a base

```bash
git switch main
git pull --ff-only origin main
```

### 2. Trabalhar na branch consolidada

```bash
git switch main
```

Para uma alteração que precise de Pull Request, uma branch temporária pode ser criada a partir da `main`,
mas deve ser removida local e remotamente depois da integração. Não manter branches de sprint ou branches
históricas no repositório remoto.

Prefixos opcionais para branches temporárias:

```text
feat/  fix/  docs/  test/  chore/
```

### 3. Commits coesos

Use Conventional Commits com escopo quando ajudar:

```text
feat(periods): associate subjects with current period
fix(auth): enforce ownership for private resources
test(sessions): cover date-range conflicts
docs(domain): document task and exam boundaries
```

Commits devem compilar e, quando possível, passar os testes relevantes. Fixups locais podem ser consolidados antes do push; histórico compartilhado não deve ser reescrito sem autorização.

### 4. Pull Request

O PR deve conter objetivo, escopo, riscos, migração de dados, validações executadas, limitações e screenshots quando houver mudança visual relevante. Use `main` como base e aguarde checks/revisão antes do merge.

Se a branch tiver um único commit coeso, merge commit ou squash produzem resultado aceitável. Se houver vários commits de correção intermediária, prefira squash no GitHub. Depois do merge, remova a branch remota quando não houver trabalho dependente.

### 5. Continuidade

Após cada entrega, atualize a `main` e continue nela. O backlog organiza histórias e prioridades, não uma
coleção de branches permanentes.

## Verificações antes do push

```bash
python -m pytest -q
python -m compileall -q app.py app_pages src tests
git diff --check
git status --short
```

Também confirme que `.env`, `.streamlit/secrets.toml`, chaves e dumps não estão rastreados.

## Política de histórico

- não usar `git reset --hard` ou force push em branches compartilhadas;
- não reescrever `main` para “embelezar” commits antigos;
- não fazer merge de `main` repetidamente numa feature sem conflito ou dependência real;
- corrigir mensagem/organização futura em vez de apagar rastreabilidade passada;
- vincular cada sprint ao respectivo PR no resumo da entrega.
