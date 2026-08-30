# Workflow Git e revisão do histórico

## Estado observado

O histórico preserva todas as entregas e PRs, mas branches antigas receberam merges intermediários de `main` e algumas histórias aparecem em mais de uma linha de integração. Isso aumenta o ruído visual, porém não justifica reescrever commits já publicados.

Decisão: preservar o histórico existente e aplicar um fluxo mais simples a partir das próximas sprints.

## Fluxo obrigatório

### 1. Atualizar a base

```bash
git switch main
git pull --ff-only origin main
```

### 2. Criar uma branch por entrega

```bash
git switch -c feat/sprint-XX-descricao
```

Prefixos usuais:

```text
feat/  fix/  docs/  test/  chore/
```

Não reutilizar branch mesclada e não misturar duas sprints independentes.

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

### 5. Próxima sprint

Não crie a próxima branch a partir de uma feature ainda aberta. Espere o merge, atualize `main` e crie a nova branch. Exceções exigem uma estratégia explícita de PRs empilhados.

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
