# Checklist e formato da auditoria

## Detecção da stack

Registre evidências para linguagem, framework web/UI, ORM/query builder ou driver, mecanismo de autenticação e autorização, frontend, testes e arquivos de deploy/configuração (Docker, CI, Helm, Terraform, secrets e variáveis de ambiente). Em Streamlit, considere páginas, widgets, callbacks, `st.session_state`, `st.cache_resource`, `st.cache_data`, `st.form`, componentes HTML/JS e ausência de backend HTTP separado.

## Categorias

### 1. Isolamento de inquilino/dono

Identifique primeiro o mecanismo real: RLS, middleware de tenant, contexto de usuário, filtro manual, repository ou outro. Depois percorra listagens, buscas, agregações, relatórios, exportações e escritas. Em uma aplicação Streamlit, cruze identidade autenticada e filtros dos services/repositories; `session_state` não é isolamento. Achado exige uma consulta ou operação real que permita acesso fora do escopo do chamador.

### 2. Permissão definida no navegador/UI

Mapeie cada gate de papel/privilégio no frontend para a operação correspondente. Em Streamlit, examine condicionais de página, botões, formulários, callbacks e services chamados. Verifique se a autorização equivalente ocorre no ponto confiável (service/backend/repository) em toda operação sensível. Não force a categoria quando não houver frontend separado; explique o equivalente analisado.

### 3. IDOR

Enumere sistematicamente todos os handlers/rotas e, em Streamlit, todos os fluxos que recebem IDs por widget, query param, estado ou formulário. Para cada busca, alteração e exclusão, confirme a posse/tenant no mesmo caminho da operação. Um ID previsível sozinho não é achado sem ausência comprovada de autorização.

### 4. Chaves expostas

Inspecione código, configurações, documentação, scripts, Docker/CI/Helm/Terraform, arquivos ignorados quando acessíveis, histórico Git e bundles gerados. Procure API keys, tokens, senhas, JWT/webhook secrets, chaves privadas, credenciais padrão e defaults públicos (`${VAR:-valor}`). Verifique validação de startup contra defaults inseguros. Redija qualquer valor no relatório; não copie segredo para evidência.

### 5. Inputs sem tratamento/XSS

Adapte os sinks à stack: `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`, `unsafe_allow_html`, markdown/HTML, URLs controladas, `eval`/`new Function`, componentes customizados e HTML de e-mails/templates/respostas. Procure a biblioteca de sanitização e confirme se ela é aplicada no caminho real. Sem frontend ou sink aplicável, declare a categoria não aplicável.

## Evidência e severidade

Cada achado deve seguir este formato:

```text
ID / Categoria / Severidade
Arquivo:linha
Trecho mínimo (sem segredos)
Condição de explorabilidade
Por que é explorável
Impacto
```

Use somente `crítica`, `alta`, `média`, `baixa` ou `informativa`. A severidade deve refletir impacto e pré-condições observáveis. Diferencie `nenhum achado verificado` de `não aplicável`. Liste também controles corretos com arquivo/linha e o que foi coberto, sem afirmar que áreas não auditadas estão protegidas.

## PDF e issues

O relatório deve incluir:

- capa com `Relatório de Auditoria de Segurança — <nome do projeto>`, data, escopo e método;
- contagem por severidade e categoria, gráficos de rosca/barras e paleta definida na skill;
- pontos fortes, pontos fracos, tabela `Severidade | Arquivo:linha | Descrição` e recomendações ordenadas;
- ao final, blocos `--- ISSUE n ---` e `--- FIM ISSUE n ---`.

Cada issue acionável deve conter:

```markdown
# [Segurança] <descrição curta da falha>

Labels sugeridas: security, <severidade>

## Problema e explorabilidade
...

## Evidência
- `arquivo:linha` — `trecho mínimo sem segredo`

## Impacto
...

## Sugestão de correção
...

## Critérios de aceite
- [ ] ...
```

Agrupe achados triviais do mesmo tema quando isso reduzir ruído sem perder evidência. Não crie issues diretamente no GitHub sem autorização explícita.

## Validação do PDF

Confirme número de páginas com `pdfinfo` ou ferramenta equivalente. Se possível, rasterize pelo menos a primeira, uma página com gráficos, uma com tabela e a última página com `pdftoppm` ou biblioteca equivalente. Verifique A4, margens próximas de 2 cm, contraste, quebra de tabelas, legibilidade, cabeçalho/rodapé e que o texto não contém tokens/credenciais. Registre limitações se alguma ferramenta não estiver disponível.
