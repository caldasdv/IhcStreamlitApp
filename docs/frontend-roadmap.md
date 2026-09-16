# Roadmap de frontend e IHC

## Revisão do estado atual

### Evidências no código

- O frontend é composto por `st.navigation`, páginas Streamlit, formulários, containers, Plotly e um Custom Component v2 com fallback nativo.
- Existe CSS global em `src/ui/styles.py`, com alguns seletores baseados em `data-testid` interno do Streamlit.
- Não há framework frontend paralelo; o componente de agenda mantém HTML, CSS e JavaScript locais e restritos à apresentação.
- A grade semanal de aulas usa Custom Component v2 para manter as ações de edição e remoção junto ao cartão, com confirmação local e retorno de eventos ao service Python.
- O dashboard usa Plotly quando há ganho de interação e oferece tabela equivalente.
- O dashboard também usa cards HTML/CSS reutilizáveis para resumir progresso por disciplina com texto equivalente às barras.
- A fundação visual usa tokens compartilhados, métricas consistentes, badges compactos e superfícies sem caixas brancas desconectadas.
- A barra lateral usa marca, conta, navegação ativa, foco visível e meta semanal em blocos distintos.
- A tela Hoje apresenta o próximo passo pendente e a agenda semanal posiciona sessões por horário e duração.
- A aplicação possui estados vazios, loading e feedback de ação, mas ainda não há avaliação com usuários.

### Inferências

- A simplicidade atual reduz risco de deploy e manutenção, mas limita hierarquia visual, responsividade e interações analíticas.
- A maior oportunidade não é trocar toda a tecnologia: é criar consistência visual e introduzir elementos externos somente onde eles resolvem uma tarefa real.

### Hipóteses a validar

- Usuários podem compreender melhor o plano com uma representação visual de calendário.
- Gráficos com hover, seleção e tooltip podem ajudar decisões de planejamento.
- Um visual mais refinado aumenta confiança, mas não deve ser tratado como resultado validado antes de teste.

## Princípios para o frontend

1. Preservar o monólito modular e o deploy no Community Cloud.
2. Preferir componentes nativos quando atendem à tarefa.
3. Adicionar dependência somente com problema, alternativa nativa, impacto de deploy e teste definidos.
4. Não colocar regra de negócio em JavaScript ou no componente visual.
5. Todo componente externo precisa de fallback, estado vazio, erro, loading, foco e alternativa textual.
6. Não usar cor como único significado e não depender de seletores internos frágeis sem necessidade.
7. Validar a interação com pessoas antes de declarar melhoria de UX.

## Estratégia de elementos externos

### Plotly

É usado para perguntas analíticas que os gráficos nativos não respondem tão bem: evolução temporal,
tooltip com unidade e comparação selecionável. A integração ocorre por `st.plotly_chart`, com dados
agregados antes da apresentação e alternativa tabular.

### Custom Component v2

Usar somente para interação que não possa ser expressa adequadamente com Streamlit, por exemplo
um calendário visual com seleção de intervalo ou uma visualização de agenda. O componente deve
receber dados já preparados pelos services e devolver apenas eventos de UI. HTML, CSS e JavaScript
devem ser confiáveis e nunca receber conteúdo não sanitizado do usuário ou do MongoDB.

### Bibliotecas de terceiros

Não adicionar `streamlit-extras`, grids ou frameworks React por padrão. Uma biblioteca poderá entrar
apenas após um spike comparando manutenção, acessibilidade, tamanho, compatibilidade com a versão
do Streamlit e comportamento no Community Cloud.

## Sprints propostas

### Sprint 8 — Fundação visual e design system leve

**Objetivo:** transformar o protótipo visual em uma interface consistente, legível e responsiva sem
introduzir frontend paralelo.

**US-011:** Como estudante quero reconhecer rapidamente hierarquia, ações e estados em todas as telas.

- Prioridade: P1
- Critérios: tokens de cor/espaçamento/tipografia documentados; componentes de cabeçalho, card, status e ação reutilizados; foco e contraste revisados; desktop e viewport estreito verificados.
- Dependências: revisão IHC, `src/ui/components` e `styles.py`.
- Complexidade: M
- Status: DONE

**Tarefas:** inventário visual; tokens; componente de status; componente de feedback; revisão de CSS; estados de loading/vazio/erro.

### Sprint 9 — Componentes de interação rica

**Objetivo:** testar um componente externo pequeno que reduza atrito em uma tarefa importante.

**US-012:** Como estudante quero navegar pelo meu plano em uma agenda visual para localizar e selecionar sessões com menos esforço.

- Prioridade: P1
- Critérios: componente mostra sessões e estado textual; seleção retorna um identificador; teclado e alternativa textual funcionam; falha do componente não impede a página; nenhum acesso direto ao MongoDB.
- Dependências: Sprint 8; spike de Custom Component v2; decisão registrada em ADR.
- Complexidade: L
- Status: DONE (spike e fallback implementados)

**Tarefas:** protótipo comparativo (Streamlit nativo versus componente); contrato de entrada/saída; fallback; segurança de HTML/JS; teste no Community Cloud.

### Sprint 10 — Dashboard analítico avançado

**Objetivo:** melhorar decisões de planejamento com visualizações interativas justificadas.

**US-013:** Como estudante quero explorar meu progresso por período e disciplina para decidir onde ajustar meu plano.

- Prioridade: P1
- Critérios: pergunta analítica explícita por gráfico; tooltip com unidade; filtros visíveis; tabela equivalente; estado sem dados; performance aceitável; dados agregados antes da UI.
- Dependências: Sprint 8; transformações de relatório; decisão sobre Plotly.
- Complexidade: M
- Status: DONE

**Tarefas:** avaliar gráficos nativos versus Plotly; adicionar somente gráficos que ganhem interação real; testar séries vazias e muitos dados; documentar dependência.

**Execução:** o dashboard passou a usar Plotly para comparação por disciplina e evolução diária,
com filtro temporal e de disciplina aplicado antes das agregações, tooltips em minutos e tabela
alternativa. A dependência foi adicionada como `plotly>=5.0`.

O detalhamento por disciplina passou a usar um componente visual leve com barras semânticas,
percentuais e minutos concluídos, mantendo os dados preparados no service e sem dependência de React.

O refinamento posterior alinhou métricas da tela Hoje, estados de sessão e fundo dos gráficos ao
mesmo sistema visual. Hover e foco foram preservados; a validação de contraste e responsividade
em navegador real continua pendente.

A grade de aulas passou a ter ações de edição e remoção no card, confirmação local e lista textual
nativa como fallback. IDs recebidos pelo componente são resolvidos contra os dados carregados antes
da operação persistente.

A agenda de sessões passou a usar uma escala temporal visual e a tela Hoje ganhou um cartão de próxima
ação com acesso direto à Semana, usando somente dados já persistidos.

### Sprint 11 — Responsividade e acessibilidade aplicada

**Objetivo:** tornar as tarefas principais utilizáveis em viewport estreito, teclado e tecnologias assistivas quando aplicável.

**US-014:** Como estudante quero usar o plano em telas menores sem perder ações ou contexto.

- Prioridade: P1
- Critérios: navegação compreensível; alvos acionáveis; formulários sem corte; tabela/gráfico com alternativa; foco perceptível; mensagens sem dependência de cor; teste manual em viewport estreito.
- Dependências: Sprints 8–10.
- Complexidade: M
- Status: DONE

**Tarefas:** percurso cognitivo; revisão de ordem de foco; densidade; labels; alternativa de dados; inspeção heurística e comunicabilidade.

**Execução:** datas completas e filtros ativos ficaram visíveis; o carregamento de sessões ganhou
recuperação com tentativa novamente; a agenda usa layout responsivo e foco de teclado; gráficos
mantêm tabela alternativa; alvos de interação receberam tamanho mínimo e a interface respeita
redução de movimento.

**Limitação:** a verificação em viewport estreito e por teclado foi estática; ainda requer avaliação
manual no navegador e teste com pessoas na Sprint 12.

### Sprint 12 — Avaliação e polimento de produto

**Objetivo:** verificar se o refinamento visual melhora tarefas reais antes de declarar o frontend concluído.

**US-015:** Como equipe quero observar estudantes usando os fluxos principais para priorizar correções baseadas em evidência.

- Prioridade: P0
- Critérios: objetivo, tarefas, perfil e consentimento definidos; evidências separadas de hipóteses; problemas classificados; correções priorizadas; limitações registradas.
- Dependências: Sprints 8–11 e acesso a participantes.
- Complexidade: M
- Status: TODO (plano preparado; depende de avaliação real)

**Tarefas:** roteiro DECIDE; teste de criar/concluir/reagendar; leitura do dashboard; viewport estreito; relatório de IHC; revisão do backlog.

O protocolo executável está em `docs/usability-test-plan.md`. A sprint não será marcada como concluída
antes da coleta e análise reais.

## Definition of Ready para frontend externo

- [ ] tarefa do usuário e pergunta de design identificadas;
- [ ] alternativa nativa comparada;
- [ ] contrato de dados e eventos definido;
- [ ] estados inicial, loading, sucesso, vazio, erro e indisponível descritos;
- [ ] acessibilidade e alternativa textual previstas;
- [ ] dependência e impacto no Community Cloud avaliados;
- [ ] conteúdo não confiável nunca será injetado no componente;
- [ ] plano de avaliação definido.

## Definition of Done para frontend externo

- [ ] interação principal funciona com dados reais e fake;
- [ ] componente não acessa services/repositories diretamente;
- [ ] fallback ou caminho alternativo existe;
- [ ] feedback e recuperação foram verificados;
- [ ] testes relevantes passam;
- [ ] bundle/dependência documentado;
- [ ] smoke test no Community Cloud passa;
- [ ] revisão de IHC registra evidências, hipóteses e limitações.

## Execução da Sprint 8

**Status:** DONE

Foi criada a primeira fundação visual reutilizável: cabeçalho de página, apresentação consistente
de estados de sessão, indicador textual e visual de disciplina, tokens CSS, foco visível, viewport
estreito e respeito a `prefers-reduced-motion`. Nenhuma dependência externa foi adicionada nesta
etapa porque a tarefa ainda era consistência visual, não interação que exigisse JavaScript.

**Limitação:** a revisão responsiva foi estática/smoke test. A avaliação com estudantes permanece
planejada para a Sprint 12.

## Execução da Sprint 9

**Status:** SPIKE CONCLUÍDO

Foi implementada uma agenda semanal visual com Custom Component v2. Ela agrupava sessões por dia,
permitia selecionar uma sessão, usava tokens de tema e possuía fallback para a lista nativa. A decisão
e os limites estão registrados em `docs/decisions/ADR-004-custom-component-v2.md`. Atualmente, a lista
nativa por abas é o fluxo principal por oferecer ações contextuais mais claras e melhor previsibilidade.

**Limitação:** ainda é necessário validar a interação no Community Cloud e com estudantes antes de
considerá-la uma substituição definitiva da visão semanal.

## Refinamento visual posterior

Foi aplicada uma extensão da fundação visual nas telas existentes: home com hero editorial e pulso
semanal, paleta compartilhada nos gráficos Plotly, superfícies e formulários, labels compactos na
navegação lateral, e acabamento coerente nos componentes de agenda e grade. A decisão mantém
Streamlit e Custom Components v2; não houve necessidade concreta de introduzir React no produto.
Essa alteração é uma decisão de design implementada, não uma validação com usuários. A avaliação
em navegador real e com estudantes continua pendente na Sprint 12.

Também foi adicionada uma faixa de ritmo semanal reutilizável na Home e na Semana, com leitura
visual de minutos concluídos/planejados por dia. Ela complementa a agenda, não substitui seus
dados detalhados, e não introduz uma nova regra de negócio ou coleção.

Na Home, foram adicionados atalhos para iniciar sessão, revisar a semana e organizar conteúdos.
A tela de conteúdos passou a apresentar subtópicos como uma trilha visual de estados, reutilizando
o progresso já persistido e sem criar nova collection.
