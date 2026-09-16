# Revisão de IHC/UX

## Escopo e método

Foi feita uma inspeção heurística estática dos fluxos de visão geral, nova sessão, visão semanal,
progresso e disciplinas. O escopo considerou usabilidade, comunicabilidade, acessibilidade,
prevenção/recuperação de erros e estados de dashboard, conforme `SKILL-IHC-UX.md`.

Não houve teste com usuários nesta revisão. A avaliação interativa e o roteiro de tarefas estão em
[`docs/usability-test-plan.md`](usability-test-plan.md); portanto, os itens marcados como hipótese
precisam ser confirmados com uso real.

## Correções aplicadas

- O dashboard agora calcula o resumo por disciplina usando a mesma semana escolhida pelo usuário.
- A semana escolhida pode ser qualquer dia; a interface informa quando ajusta a visualização para a segunda-feira correspondente.
- O dashboard oferece tabela com os mesmos dados dos gráficos, incluindo unidade e contagens.
- Consultas e ações de escrita exibem recuperação compreensível e registram a exceção no log sem expor infraestrutura.
- Estados sem disciplinas e falhas de carregamento receberam caminhos explícitos.
- Indicadores de status continuam acompanhados por texto, e o contraste de captions foi reforçado.
- Foi adicionada indicação visual da cor da disciplina com o valor hexadecimal legível.
- Foi preservada a confirmação antes da exclusão.
- A navegação foi agrupada por atividade e a área principal passou a ser chamada de “Hoje”.
- A visão semanal deixou de duplicar a mesma informação em agenda customizada e lista nativa; a lista
  acionável é agora a representação principal.
- O formulário de nova sessão deixou de usar três colunas, reduzindo risco de corte e compressão em
  telas estreitas.
- A conclusão de uma sessão passou a ficar no próprio card da sessão na tela Hoje, reduzindo a
  necessidade de selecionar novamente o item em um controle separado.
- A fundação visual foi alinhada a uma identidade de estudo com hierarquia de tipografia, contraste,
  superfícies e ação primária consistentes entre as telas.
- O fundo do tema, os cards, os inputs e as métricas passaram a usar uma escala coerente de superfícies,
  reduzindo os blocos brancos desconectados.
- Os cards de sessão passaram a separar visualmente horário, disciplina, assunto e objetivo.
- A visão semanal passou a resumir a carga no topo e organizar os dias em abas, reduzindo a coluna
  vertical de sete blocos e mantendo a conclusão no card da sessão.
- A tela Hoje passou a orientar o primeiro uso com ações sequenciais para criar período e disciplina;
  bloqueios da tela Nova sessão também oferecem a ação de recuperação correspondente.
- A visão semanal passou a permitir navegar para a semana anterior, atual ou seguinte.

## Achados ainda pendentes

| ID | Classificação | Achado | Próxima avaliação |
|---|---|---|---|
| IHC-002 | Resolvido tecnicamente / validar | Google OIDC e isolamento por `provider + subject` foram implementados. | Confirmar login, logout e isolamento com duas contas no Community Cloud. |
| IHC-007 | Médio | Editar/excluir está disponível na visão geral, mas não na visão semanal. | Observar a tarefa de correção do plano e decidir se ações rápidas são necessárias. |
| IHC-010 | Médio / hipótese | CSS usa seletores internos do Streamlit e pode variar após atualização. | Verificar visualmente no Community Cloud após cada atualização relevante. |
| IHC-011 | Alto | A visão semanal duplicava a agenda visual e a lista, dificultando identificar a representação principal. | Corrigido tecnicamente; validar a compreensão da semana em teste com usuários. |
| IHC-012 | Médio | O formulário de nova sessão distribuía campos em três colunas sem evidência de comportamento adequado em celular. | Corrigido tecnicamente; verificar em viewport estreito e teclado. |
| IHC-013 | Alto | A ação de concluir ficava separada do card e exigia uma segunda seleção da sessão. | Corrigido tecnicamente; validar tempo e erros na tarefa de registrar estudo. |
| IHC-014 | Médio | A interface usava a aparência padrão do Streamlit com pouca diferenciação entre hierarquia e ações. | Corrigido tecnicamente; validar legibilidade, contraste e compreensão visual no navegador. |
| IHC-015 | Médio | O tema e o CSS usavam fundos diferentes, criando áreas brancas visualmente desconectadas. | Corrigido tecnicamente; validar em todas as páginas e temas do Community Cloud. |
| IHC-016 | Alto | A visão semanal empilhava sete blocos de dias, dificultando comparação e aumentando o deslocamento vertical. | Corrigido tecnicamente; validar compreensão da semana e localização do dia atual. |
| IHC-017 | Alto | Usuários sem período ou disciplina encontravam bloqueios sem orientação sequencial na tela Hoje e em Nova sessão. | Corrigido tecnicamente; validar o primeiro uso completo sem instrução externa. |
| IHC-018 | Médio | A visão semanal não permitia consultar semanas anteriores ou futuras. | Corrigido tecnicamente; validar se a navegação preserva o contexto esperado. |
| IHC-019 | Alto | Disciplinas eram exibidas como uma lista simples e não podiam ser editadas. | Corrigido tecnicamente; validar compreensão da edição e prevenção de duplicidade. |
| IHC-020 | Alto | A grade de aulas empilhava horários por dia, com pouca visão de conjunto e muito deslocamento vertical. | Corrigido tecnicamente; validar localização de aulas e remoção no celular. |
| IHC-021 | Alto | A primeira reorganização em abas ainda não oferecia uma leitura visual simultânea dos sete dias. | Corrigido tecnicamente; validar leitura da grade e rolagem horizontal em telas estreitas. |
| IHC-022 | Alto | A visão semanal de sessões ainda escondia cada dia em abas, dificultando a comparação da carga planejada. | Corrigido tecnicamente; validar seleção da sessão, leitura dos sete dias e rolagem no celular. |

## Plano de avaliação seguinte

1. Observar uma pessoa criando uma sessão, corrigindo um conflito e concluindo a sessão.
2. Observar a leitura do progresso com uma semana contendo sessões concluídas e atrasadas.
3. Repetir em viewport estreito e com navegação por teclado.
4. Registrar tempo, erros, dúvidas verbalizadas e conclusão da tarefa, sem declarar preferência sem evidência.
