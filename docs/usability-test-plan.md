# Plano de teste de usabilidade e IHC — Sprint 12

## Objetivo

Verificar se estudantes conseguem planejar, corrigir, executar e interpretar seu plano de estudos
com a versão atual, incluindo a agenda visual e o dashboard Plotly.

Este documento é um plano. Não contém resultados de usuários.

## Perguntas de avaliação

1. Uma pessoa nova entende como começar e criar uma sessão?
2. Ela consegue perceber e recuperar um conflito de horário?
3. Ela encontra uma sessão na agenda e entende o estado dela?
4. Ela consegue concluir uma sessão e confirmar o resultado após o rerun?
5. Ela interpreta corretamente os filtros, unidades e dados do dashboard?
6. Os fluxos permanecem compreensíveis em viewport estreito e com teclado?

## Método (DECIDE)

- **D — Objetivos:** avaliar aprendizado, compreensão de estados, recuperação e leitura analítica.
- **E — Perguntas:** usar as seis perguntas acima, sem conduzir a resposta.
- **C — Coleta:** teste moderado individual, observação e think aloud opcional; registrar sucesso, erros, tempo e dúvidas.
- **I — Questões práticas:** ambiente real ou remoto, navegador atual, dados fictícios e conta de teste isolada.
- **D — Ética:** participação voluntária, consentimento antes da sessão, possibilidade de desistir e nenhuma senha/dado pessoal real coletado.
- **E — Avaliação:** separar observação, interpretação, hipótese e recomendação; priorizar por frequência, impacto e recuperação.

## Participantes

Recrutar de 3 a 5 estudantes ou pessoas que realizem planejamento de estudos com frequência.
Registrar apenas características que influenciem a avaliação: experiência com ferramentas de
planejamento, frequência de estudo, dispositivo usado e familiaridade com dashboards. Não tratar
este grupo pequeno como representativo de todos os estudantes.

## Roteiro

### Abertura

Explicar que o produto está sendo avaliado, não a pessoa. Pedir consentimento para observação e,
se aplicável, gravação. Não ensinar o caminho antes da tarefa.

### Tarefas

1. Entre com sua conta e explique o que você entende da tela inicial.
2. Crie uma sessão de 45 minutos para uma disciplina.
3. Tente criar outra sessão em horário conflitante e explique o que faria após a mensagem.
4. Encontre a sessão na visão semanal e selecione-a na agenda visual.
5. Conclua a sessão e diga como sabe que a ação funcionou.
6. Abra o progresso, escolha outra semana e uma disciplina; explique os gráficos e a tabela.
7. Repita as tarefas 4 e 6 em viewport estreito e, quando possível, navegue por teclado.

### Encerramento

Perguntar o que foi mais fácil, o que causou dúvida, o que faltou e o que a pessoa esperava que
acontecesse. Não induzir preferência por componente nativo ou externo.

## Métricas e registros

Por tarefa, registrar:

- concluída sem ajuda / com ajuda / não concluída;
- tempo aproximado;
- erros e tentativas de recuperação;
- dúvidas ou rupturas comunicativas;
- estado do dispositivo e viewport;
- observação literal, sem transformar comentário isolado em regra.

Não usar tempo como única medida de qualidade. Uma tarefa rápida com interpretação errada não é
sucesso.

## Formulário de achado

```text
ID:
Tarefa/local:
Observação:
Evidência:
Interpretação:
Hipótese:
Impacto:
Frequência:
Recuperação possível:
Severidade:
Recomendação:
Limitação:
```

## Critério de decisão

Após as sessões, priorizar problemas que impeçam tarefa essencial, causem interpretação errada ou
não ofereçam recuperação. Preferências visuais sem impacto em tarefa devem ser registradas como
oportunidades, não como defeitos críticos.

## Limitações atuais

- Ainda não há participantes, resultados ou amostra coletada.
- O teste depende de uma conta de teste e de ambiente Cloud configurado.
- A avaliação de acessibilidade por tecnologia assistiva requer escopo e participantes específicos.
