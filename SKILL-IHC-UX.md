---
name: ihc-ux
description: >
  Skill de Interação Humano-Computador (IHC) e Experiência do Usuário (UX) para agentes
  de desenvolvimento, produto e design. Use ao analisar requisitos, planejar interfaces,
  modelar interação, construir protótipos, implementar UI, revisar fluxos, avaliar
  usabilidade, acessibilidade, comunicabilidade e experiência do usuário. A base conceitual
  desta skill é o livro "Interação Humano-Computador e Experiência do Usuário", de Simone
  D. J. Barbosa, Bruno Santana da Silva, Milene Selbach Silveira, Isabela Gasparini,
  Ticianne Darin e Gabriel D. J. Barbosa.
---

# IHC/UX — Design, Implementação e Avaliação de Sistemas Interativos

## 0. Propósito da skill

Esta skill transforma fundamentos de IHC/UX em regras operacionais para um agente que participa
do desenvolvimento de sistemas interativos.

Seu papel NÃO é apenas "melhorar o visual".

Seu papel é garantir que decisões de produto, interação e interface sejam coerentes com:

- as pessoas que utilizarão o sistema;
- seus objetivos;
- suas atividades e tarefas;
- seu contexto de uso;
- suas capacidades e limitações;
- a linguagem e os conceitos que conhecem;
- os efeitos esperados e inesperados da tecnologia;
- a qualidade de uso esperada;
- evidências obtidas por análise e avaliação.

A interface não é uma camada decorativa sobre a arquitetura. Ela é o ponto pelo qual pessoas
interpretam, controlam e se apropriam do sistema.

---

# 1. Regra fundamental: projetar de fora para dentro

Ao receber uma solicitação de feature, página, dashboard, formulário, fluxo ou sistema, NÃO comece
automaticamente pelo banco de dados, API, componentes ou layout.

Primeiro investigue o mundo em que o sistema será usado.

A sequência preferencial é:

1. identificar stakeholders;
2. identificar usuários;
3. compreender objetivos;
4. compreender atividades e contexto;
5. identificar necessidades e problemas;
6. definir requisitos de IHC;
7. organizar o espaço de problema;
8. modelar conceitos, tarefas e interação;
9. explorar alternativas;
10. projetar a interface;
11. avaliar;
12. implementar;
13. avaliar novamente;
14. iterar.

Engenharia de software e IHC devem trabalhar juntas, mas não são equivalentes.

Um sistema pode possuir boa arquitetura, testes, desempenho e ausência de falhas e ainda assim
possuir baixa qualidade de uso.

---

# 2. Postura obrigatória do agente

Sempre:

- diferencie fatos, evidências, inferências, hipóteses e decisões;
- evite inventar comportamento de usuário;
- não invente resultado de entrevista, teste ou pesquisa;
- não trate preferência pessoal do desenvolvedor como requisito de UX;
- explicite suposições quando não houver dados;
- considere alternativas de design antes de escolher uma solução;
- avalie consequências positivas e negativas da intervenção;
- preserve controle e autonomia do usuário;
- projete prevenção, recuperação e tolerância a erros;
- considere acessibilidade desde o início;
- mantenha consistência entre modelo conceitual, interação e interface;
- planeje avaliação antes de declarar a solução concluída.

Quando informação essencial estiver ausente, o agente deve fazer a menor quantidade de perguntas
necessária ou trabalhar com hipóteses claramente rotuladas.

---

# 3. Objetos de estudo de IHC aplicados ao projeto

Analise o sistema em cinco dimensões inter-relacionadas.

## 3.1 Natureza da interação

Investigue o que acontece entre usuário e sistema.

Pergunte:

- Qual é o objetivo do usuário?
- Como esse objetivo se transforma em intenção?
- Que ações a interface permite?
- Como o sistema responde?
- O usuário percebe a resposta?
- Ele consegue interpretá-la?
- Ele entende se avançou em direção ao objetivo?
- Onde podem surgir rupturas?

Não reduza interação a eventos de clique.

## 3.2 Uso e contexto de uso

Investigue:

- onde o sistema é utilizado;
- quando;
- por quem;
- com que frequência;
- em quais dispositivos;
- sob quais condições ambientais;
- com quais restrições de conectividade;
- com quais interrupções;
- com quais outros sistemas e artefatos;
- com quais outras pessoas;
- sob quais normas organizacionais;
- dentro de qual cultura e vocabulário.

Nunca assuma que o contexto do desenvolvedor é igual ao contexto de uso.

## 3.3 Características humanas

Considere:

- percepção;
- atenção;
- memória;
- aprendizado;
- raciocínio;
- experiência prévia;
- capacidades motoras;
- visão;
- audição;
- linguagem;
- emoção;
- motivação;
- vieses cognitivos;
- diferenças individuais.

A solução deve aproveitar capacidades humanas e respeitar limitações.

## 3.4 Sistema e arquitetura da interface

Considere:

- dispositivos de entrada e saída;
- estilos de interação;
- estados;
- controles;
- navegação;
- feedback;
- representação da informação;
- mensagens;
- ajuda;
- recursos de recuperação;
- relação entre interface e modelo conceitual.

## 3.5 Processo de desenvolvimento

Garanta a presença de:

- análise;
- síntese;
- exploração de alternativas;
- prototipação;
- avaliação;
- iteração;
- registro de decisões.

---

# 4. Conceitos básicos

## 4.1 Interação

Entenda interação como um processo, não como um componente.

Use este ciclo de raciocínio:

**objetivo → intenção → ação → execução → mudança de estado → percepção → interpretação → avaliação**

Analise os dois lados:

### Execução
O usuário consegue descobrir o que fazer e como fazer?

### Avaliação
O usuário consegue perceber e compreender o que aconteceu?

---

## 4.2 Interface

Considere interface como o conjunto de meios pelos quais usuário e sistema entram em contato.

Inclui:

- elementos visuais;
- texto;
- som;
- voz;
- gestos;
- controles;
- mensagens;
- navegação;
- estados;
- comportamentos;
- feedback;
- ajuda.

Não limite "interface" ao layout.

---

## 4.3 Affordance

Um elemento deve sugerir corretamente as operações possíveis.

Verifique:

- botão parece acionável?
- link parece navegável?
- campo parece editável?
- texto somente leitura evita parecer editável?
- drag-and-drop possui pistas suficientes?
- o elemento gera uma expectativa que não será cumprida?

Evite **falsas affordances**.

A aparência de um componente não deve comunicar uma ação inexistente.

---

# 5. Critérios de qualidade em IHC

A qualidade de uso deve ser considerada por quatro perspectivas:

1. usabilidade;
2. experiência do usuário;
3. acessibilidade;
4. comunicabilidade.

Nenhuma delas deve ser reduzida a estética.

---

# 6. Usabilidade

Analise a possibilidade de o usuário utilizar o sistema para alcançar seus objetivos.

Considere:

- facilidade de aprendizado;
- facilidade de recordação;
- eficiência;
- segurança;
- prevenção de erros;
- recuperação de erros;
- satisfação.

## Checklist de usabilidade

Antes de aprovar uma interação, responda:

- Um usuário novo entende por onde começar?
- Os termos utilizados pertencem ao domínio do usuário?
- A sequência da tarefa faz sentido?
- Existem passos dispensáveis?
- O sistema exige memorização evitável?
- Ações frequentes são rápidas?
- Estados importantes são visíveis?
- O sistema informa o resultado das ações?
- É possível cancelar?
- É possível voltar?
- É possível desfazer quando apropriado?
- Os erros são prevenidos quando possível?
- Quando ocorrem, existe caminho claro de recuperação?
- O usuário preserva seu trabalho quando algo falha?

---

# 7. Experiência do Usuário — UX

Não trate UX como sinônimo de usabilidade.

Considere a experiência completa relacionada ao produto, incluindo:

- expectativas;
- emoções;
- afeto;
- prazer;
- frustração;
- confiança;
- valor percebido;
- estética;
- significado;
- lembranças;
- consequências do uso.

Pergunte:

### Antes do uso
- Que expectativa existe?
- O usuário confia no produto?
- O valor está claro?

### Durante
- Há sensação de controle?
- Há frustração evitável?
- A interação parece adequada ao objetivo?

### Depois
- O usuário sente que alcançou o que precisava?
- Qual impressão permanece?
- A experiência incentiva ou desencoraja novo uso?

Não tente "otimizar emoção" de forma manipulativa.

---

# 8. Acessibilidade

Acessibilidade é critério de qualidade de uso.

Ao desenvolver interfaces, investigue barreiras relacionadas a:

- visão;
- audição;
- movimento;
- percepção;
- cognição;
- linguagem;
- tecnologias assistivas;
- dispositivo e ambiente.

Princípios operacionais:

- não dependa apenas de cor;
- preserve contraste e legibilidade;
- utilize estrutura semântica;
- associe rótulos a controles;
- mantenha ordem de foco coerente;
- permita operação por teclado quando aplicável;
- forneça alternativas textuais;
- produza mensagens compreensíveis;
- evite ações que exijam precisão motora excessiva;
- não remova indicação de foco;
- use padrões de acessibilidade adequados à plataforma.

A aplicação de padrões técnicos deve complementar, não substituir, a avaliação da experiência real.

---

# 9. Comunicabilidade

Trate a interação como comunicação mediada pela interface.

A interface deve ajudar o usuário a entender:

- para quem o sistema parece ter sido criado;
- o que ele pode fazer;
- como pode fazer;
- por que determinada ação existe;
- quais informações precisa fornecer;
- o que aconteceu;
- o que pode acontecer em seguida;
- como se recuperar de problemas.

Procure rupturas comunicativas como:

- "O que é isto?"
- "Onde estou?"
- "O que eu faço agora?"
- "Por que isso aconteceu?"
- "Onde está a função que eu esperava?"
- "Posso fazer de outro jeito?"
- "Funcionou?"
- "Como volto?"

Se o usuário precisa realizar tentativa e erro apenas para descobrir o significado da interface,
trate isso como problema de design.

---

# 10. Fatores humanos

## 10.1 Percepção

Use a organização visual para apoiar percepção e interpretação.

Considere princípios gestálticos como:

- proximidade;
- similaridade;
- continuidade;
- simetria;
- destino comum;
- fechamento.

Use agrupamentos para comunicar relações reais.

Não crie agrupamentos visuais que contradigam a estrutura conceitual.

---

## 10.2 Percepção de cores

Ao utilizar cor:

- não dependa exclusivamente dela para transmitir significado;
- mantenha contraste;
- use significados consistentemente;
- evite excesso;
- considere diferenças perceptivas;
- combine cor com texto, forma, ícone ou posição quando necessário.

---

## 10.3 Cognição

Minimize carga cognitiva desnecessária.

Prefira:

- reconhecimento a recordação;
- pistas visíveis;
- linguagem familiar;
- agrupamentos coerentes;
- informações relevantes no momento certo;
- feedback perceptível;
- progressão clara.

Não obrigue o usuário a compreender a arquitetura interna para utilizar o produto.

---

## 10.4 Vieses cognitivos

Considere que decisões humanas podem ser influenciadas por vieses.

Nunca utilize vieses deliberadamente para induzir decisões prejudiciais ou contrárias ao interesse
do usuário.

Ao revisar escolhas, preços, defaults, confirmações ou recomendações, pergunte se o design preserva
decisão informada.

---

## 10.5 Afeto e emoção

Considere que cognição e afeto participam da experiência.

Avalie se o design pode produzir:

- segurança;
- confiança;
- prazer;
- curiosidade;
- domínio;
- ansiedade;
- frustração;
- sensação de perda de controle.

Não conclua que uma interface "bonita" necessariamente produz boa UX.

---

# 11. Abordagens teóricas como ferramentas de análise

Use teorias para raciocinar sobre problemas. Não as transforme em regras universais.

---

## 11.1 Lei de Hick-Hyman

Útil ao analisar escolhas entre alternativas.

Quando muitas opções disputam a atenção do usuário:

- verifique se todas precisam aparecer simultaneamente;
- agrupe alternativas relacionadas;
- estabeleça hierarquia;
- considere divulgação progressiva;
- priorize escolhas mais relevantes.

Não conclua mecanicamente que "menos opções sempre é melhor".

---

## 11.2 Lei de Fitts

Considere tamanho e distância de alvos de interação.

Ações importantes, frequentes ou urgentes devem ser fáceis de atingir.

Evite:

- alvos pequenos;
- controles excessivamente próximos;
- precisão motora desnecessária.

---

## 11.3 Engenharia Cognitiva

Considere:

- modelo de design;
- imagem do sistema;
- modelo construído pelo usuário.

Busque reduzir diferenças entre:

**o que o usuário pretende fazer**  
e  
**o que a interface permite descobrir e executar**

e entre:

**o estado real do sistema**  
e  
**o que o usuário consegue perceber e interpretar**.

Use a teoria da ação para analisar execução e avaliação.

---

## 11.4 Ação situada e abordagens etnometodológicas

Não presuma que atividades reais seguem perfeitamente procedimentos abstratos.

Pessoas adaptam ações ao contexto.

Ao projetar ferramentas de trabalho, observe práticas reais, exceções, improvisações, colaboração
e uso combinado de artefatos.

---

## 11.5 Análise da conversação

Ao projetar interações conversacionais ou sequenciais, considere:

- turnos;
- iniciativa;
- continuidade;
- expectativas;
- sinais de conclusão;
- reparação de falhas de entendimento.

---

## 11.6 Teoria da Atividade

Quando a tecnologia participa de uma atividade ampla, investigue:

- sujeito;
- objeto/motivo;
- instrumentos;
- regras;
- comunidade;
- divisão de trabalho;
- contradições;
- transformações da atividade.

Não isole o clique do propósito da atividade.

---

## 11.7 Cognição Distribuída

Quando várias pessoas, artefatos ou sistemas participam do raciocínio, analise como informação é
representada, transformada e compartilhada entre eles.

Considere:

- pessoas;
- telas;
- documentos;
- planilhas;
- sistemas;
- dispositivos;
- ambiente.

---

## 11.8 Engenharia Semiótica

Trate o sistema como artefato intelectual e meio de comunicação.

O agente deve avaliar se o produto comunica a visão do designer sobre:

- quem são os usuários;
- o que desejam realizar;
- por que;
- como;
- quais alternativas possuem;
- como o sistema deve ser utilizado.

Use essa perspectiva especialmente para investigar comunicabilidade.

---

# 12. Processo de Design de IHC

Design envolve:

- análise da situação;
- síntese de alternativas;
- avaliação;
- reflexão;
- refinamento.

O processo deve ser iterativo.

Não existe obrigação de uma sequência rígida única.

---

# 13. Processos e abordagens de design contemplados

A skill deve reconhecer e utilizar, quando apropriado:

- ciclo de vida em estrela;
- engenharia de usabilidade de Nielsen;
- engenharia de usabilidade de Mayhew;
- design contextual;
- design baseado em cenários;
- design dirigido por objetivos;
- design centrado na comunicação.

Não aplique uma abordagem apenas pelo nome. Escolha com base no problema, maturidade do projeto,
acesso aos usuários, riscos e recursos disponíveis.

---

# 14. Ciclo de vida em estrela

Trate avaliação como atividade central.

Após uma atividade relevante de design:

1. examine o resultado;
2. compare-o aos objetivos;
3. avalie problemas;
4. determine a próxima atividade.

O processo pode iniciar por diferentes pontos conforme a situação do projeto.

---

# 15. Exploração de alternativas

Evite convergência prematura.

Para problemas importantes:

1. formule pelo menos duas alternativas plausíveis;
2. explicite vantagens e desvantagens;
3. compare com objetivos e contexto;
4. escolha conscientemente;
5. registre a justificativa.

Quando possível, designers diferentes podem explorar alternativas independentes antes da consolidação.

---

# 16. Participação dos usuários

Envolva usuários cedo quando possível.

Quanto mais cedo o projeto obtiver contato com usuários e suas interpretações, mais cedo poderá:

- compreender necessidades;
- detectar premissas incorretas;
- avaliar alternativas;
- corrigir problemas;
- melhorar qualidade de uso.

Não substitua participação real por personas inventadas.

---

# 17. Integração com Engenharia de Software

Cada requisito importante deve ser observado por duas perspectivas.

## Perspectiva de construção

- arquitetura;
- dados;
- regras de negócio;
- APIs;
- segurança;
- desempenho;
- testes;
- manutenção.

## Perspectiva de uso

- usuário;
- objetivo;
- atividade;
- contexto;
- tarefa;
- interação;
- interface;
- experiência;
- acessibilidade;
- comunicabilidade.

Nenhuma das duas substitui a outra.

---

# 18. IHC em processos ágeis

Não trate UX como uma grande fase anterior ao desenvolvimento.

Inclua atividades de IHC continuamente no backlog.

Exemplos:

- pesquisa;
- entrevista;
- observação;
- análise;
- elaboração de persona;
- criação de cenário;
- modelagem de tarefa;
- prototipação;
- inspeção;
- teste de usabilidade;
- correção de problemas;
- avaliação de uma feature entregue.

Para histórias de usuário relevantes, inclua critérios de qualidade de uso nos critérios de aceite.

---

# 19. Identificação de necessidades e requisitos de IHC

Nunca pule diretamente para solução quando o problema ainda é desconhecido.

O erro mais grave é tomar decisões com dados incompletos ou pouco confiáveis sem reconhecer essa
limitação.

---

# 20. Planejamento da coleta de dados

Antes de coletar dados, responda:

- Que decisão precisamos tomar?
- Que pergunta precisamos responder?
- Que dados são necessários?
- De quem devem ser obtidos?
- Qual método é adequado?
- Como serão analisados?
- Quais riscos éticos existem?

---

# 21. O que investigar sobre usuários

Dependendo do projeto, investigue:

- papel e função;
- experiência;
- formação;
- conhecimento do domínio;
- conhecimento tecnológico;
- objetivos;
- tarefas;
- frequência das tarefas;
- importância;
- consequências de erros;
- ambiente;
- ferramentas;
- linguagem;
- jargão;
- motivações;
- colaboração;
- restrições;
- estratégias atuais;
- dificuldades;
- necessidades;
- desejos.

Não colete dados irrelevantes apenas para preencher uma persona.

---

# 22. Fontes de dados

Priorize fontes:

- relevantes;
- confiáveis;
- representativas.

Considere:

- usuários finais;
- stakeholders;
- especialistas do domínio;
- suporte;
- documentação;
- sistemas existentes;
- registros de problemas;
- dados de uso;
- ambiente real.

Não assuma que gestor e usuário final possuem a mesma perspectiva.

---

# 23. Ética em pesquisa com pessoas

Ao conduzir atividades envolvendo pessoas:

- explique objetivos e procedimento;
- obtenha consentimento quando necessário;
- preserve voluntariedade;
- respeite desistência;
- cuide da privacidade;
- minimize coleta de dados;
- evite desconforto;
- trate participantes com respeito;
- deixe claro que o produto está sendo avaliado, não a pessoa.

Nunca falsifique consentimento, observação ou resultado.

---

# 24. Métodos de coleta

## 24.1 Entrevistas

Use para aprofundar:

- experiências;
- práticas;
- motivações;
- expectativas;
- problemas;
- explicações.

Estruture quando apropriado:

1. apresentação;
2. aquecimento;
3. corpo principal;
4. desaceleração;
5. conclusão.

Evite perguntas indutoras.

---

## 24.2 Questionários

Use quando precisar de coleta estruturada com muitas pessoas.

Podem incluir:

- múltipla escolha;
- escalas;
- faixas;
- questões abertas.

Não escolha questionário apenas por ser mais fácil de distribuir.

---

## 24.3 Grupos de foco

Use quando opiniões e interações entre participantes forem relevantes.

Observe concordâncias, conflitos e perspectivas diferentes.

---

## 24.4 Brainstorming de necessidades e desejos

Use para expandir possibilidades.

Resultado de brainstorming é material para investigação, não prova de requisito.

---

## 24.5 Classificação de cartões

Use para investigar:

- agrupamentos;
- categorias;
- terminologia;
- arquitetura da informação.

---

## 24.6 Estudos de campo

Observe:

- ambiente;
- práticas;
- artefatos;
- interrupções;
- exceções;
- comunicação;
- dependências.

---

## 24.7 Investigação contextual

Combine observação do trabalho real com perguntas feitas no contexto da atividade.

---

# 25. Análise dos dados coletados

Antes de interpretar:

1. organize os dados;
2. verifique qualidade;
3. identifique dados incompletos;
4. prepare registros;
5. procure padrões;
6. identifique divergências;
7. relacione achados às perguntas de pesquisa;
8. separe observação de interpretação.

Nunca transforme um caso isolado automaticamente em regra universal.

---

# 26. Evidência, inferência, hipótese e decisão

Use explicitamente estas categorias:

**Evidência**  
Algo observado ou coletado.

**Inferência**  
Interpretação apoiada por uma ou mais evidências.

**Hipótese**  
Explicação ou necessidade ainda não validada.

**Requisito**  
Condição que a solução deve atender.

**Decisão de design**  
Escolha feita pela equipe.

**Restrição**  
Limitação do projeto.

Essa distinção deve aparecer em documentos de descoberta e decisões importantes.

---

# 27. Organização do espaço de problema

Use representações adequadas para organizar o conhecimento:

- perfil de usuário;
- personas;
- cenários;
- análise de tarefas;
- HTA;
- GOMS;
- CTT.

A representação é um instrumento para pensar, não um fim burocrático.

---

# 28. Perfil de usuário

Registre somente características que influenciem o projeto.

Exemplos:

- papel;
- experiência;
- formação;
- frequência de uso;
- tarefas;
- habilidades;
- limitações;
- ambiente.

Use perfis também para orientar recrutamento de participantes.

---

# 29. Personas

Personas representam grupos relevantes de usuários.

Podem incluir:

- identidade;
- status;
- objetivos;
- habilidades;
- tarefas;
- contexto;
- relacionamentos;
- expectativas;
- dificuldades.

Regra essencial:

**Persona não é sinônimo de objetivo.**

Objetivo descreve o que uma pessoa deseja alcançar. Tarefa descreve uma maneira de tentar alcançar
o objetivo.

Se uma persona não vier de pesquisa real, marque-a como **proto-persona/hipótese**.

---

# 30. Cenários

Cenário é uma narrativa concreta de uma pessoa realizando uma atividade em determinado contexto.

Use cenários para preservar a riqueza da situação de uso.

Modelo recomendado:

## Cenário
**Ator:**  
**Perfil/persona:**  
**Objetivo:**  
**Contexto:**  
**Situação inicial:**  
**Motivação:**  
**Ações:**  
**Artefatos envolvidos:**  
**Interrupções/condições:**  
**Problemas:**  
**Resultado:**  
**Como o usuário sabe que teve sucesso:**  

Um cenário representa um caminho concreto. Não precisa conter todas as alternativas abstratas de um
caso de uso.

---

# 31. Análise de tarefas

Use análise de tarefas para compreender:

- o que as pessoas fazem;
- como;
- em qual ordem;
- por que;
- com quais objetivos;
- com quais estratégias.

Não reduza análise de tarefa a uma lista de botões.

---

## 31.1 HTA — Análise Hierárquica de Tarefas

Útil para decompor objetivos em subtarefas.

Modelo:

Objetivo 0  
├── tarefa 1  
├── tarefa 2  
│   ├── tarefa 2.1  
│   └── tarefa 2.2  
└── tarefa 3  

Registre o plano que determina quando cada subtarefa ocorre.

---

## 31.2 GOMS

Use quando for importante analisar procedimentos e eficiência.

Modele:

- Goals;
- Operators;
- Methods;
- Selection Rules.

GOMS é especialmente útil quando existem diferentes métodos para alcançar o mesmo objetivo.

---

## 31.3 CTT

Use ConcurTaskTrees quando relações temporais, concorrência ou coordenação entre tarefas forem
importantes.

Não utilize CTT se o nível de formalidade não trouxer benefício.

---

# 32. Design de IHC

O design deve articular:

- objetivos;
- conceitos;
- tarefas;
- interação;
- interface.

Não comece pelo pixel.

---

# 33. Design conceitual

Defina primeiro **o que** o produto permite fazer e **quais conceitos** o usuário precisa compreender.

Depois defina como a solução será materializada.

Analise:

- entidades do domínio;
- atributos;
- relações;
- ações;
- estados;
- responsabilidades;
- conceitos familiares;
- metáforas adequadas.

Pergunta obrigatória:

**Qual modelo conceitual o usuário construirá ao utilizar esta interface?**

---

# 34. Modelo conceitual

Evite copiar diretamente estruturas do banco para a interface.

A organização conceitual deve fazer sentido para o usuário.

Pode se apoiar em:

- atividades;
- objetos familiares;
- espaços;
- conversas;
- metáforas;
- relações do domínio.

Metáforas devem ajudar, não limitar artificialmente a solução.

---

# 35. Cenários de interação

Antes de codificar fluxos críticos, represente a interação.

Modelo:

**Usuário:**  
**Objetivo:**  
**Pré-condições:**  
**Início:**  
**Fluxo principal:**  
**Alternativas:**  
**Erros possíveis:**  
**Resposta do sistema:**  
**Recuperação:**  
**Estado final:**  

---

# 36. Design centrado na comunicação

Modele a interação considerando-a como conversa entre usuário e sistema.

Garanta coerência entre:

- conteúdo;
- sequência;
- controles;
- mensagens;
- estados;
- ajuda.

Antecipe rupturas e ofereça reparação.

---

# 37. Modelagem da interação

Para sistemas suficientemente complexos, considere representações específicas de interação, como
MoLIC, quando elas ajudarem a raciocinar sobre:

- objetivos;
- diálogos;
- transições;
- alternativas;
- recuperação de falhas.

Não gere um diagrama apenas para cumprir processo.

---

# 38. Design da interface

Somente após compreender objetivos, tarefas, conceitos e interação, detalhe:

- layout;
- componentes;
- navegação;
- conteúdo;
- tipografia;
- feedback;
- estados;
- ícones;
- comportamento responsivo.

Interface deve materializar o modelo conceitual e a interação de forma compreensível.

---

# 39. Estilos de interação

Escolha conscientemente entre estilos adequados ao contexto, como:

- linguagem de comando;
- menus;
- formulários;
- manipulação direta;
- perguntas e respostas;
- linguagem natural;
- interação multimodal.

Não escolha estilo apenas por tendência tecnológica.

---

# 40. Representações da interface

Utilize fidelidade compatível com a pergunta que precisa responder.

Possíveis representações:

- sketch;
- wireframe;
- storyboard;
- protótipo em papel;
- mockup;
- protótipo navegável;
- implementação parcial.

Não invista em alta fidelidade quando o conceito ainda está instável.

---

# 41. Sistema de ajuda

Ajuda não deve compensar uma interação mal projetada.

Quando necessária:

- seja fácil de encontrar;
- seja focada na tarefa;
- use linguagem do usuário;
- forneça passos concretos;
- seja concisa;
- esteja disponível no momento relevante.

---

# 42. Sistemas adaptáveis e adaptativos

Se o sistema permite personalização ou adaptação automática:

- deixe claro o que pode mudar;
- preserve previsibilidade;
- ofereça controle;
- explique adaptações relevantes;
- permita ajustar ou reverter comportamentos quando adequado.

---

# 43. Princípios e diretrizes gerais de design

Diretrizes são recomendações, não leis universais.

Sempre considere contexto e possíveis conflitos.

---

## 43.1 Correspondência com expectativas dos usuários

Use:

- conceitos familiares;
- linguagem do domínio;
- comportamento previsível;
- convenções conhecidas.

Não viole expectativa consolidada sem benefício claro.

---

## 43.2 Simplicidade nas estruturas das tarefas

Reduza complexidade que não contribui para o objetivo.

Considere:

- automação apropriada;
- redução de passos;
- agrupamento;
- defaults;
- reorganização da tarefa.

Não remova controle necessário em nome da simplicidade.

---

## 43.3 Controle e liberdade

O usuário deve sentir que conduz a interação.

Ofereça quando apropriado:

- cancelar;
- voltar;
- desfazer;
- editar;
- revisar;
- sair;
- recusar.

Equilibre liberdade com restrições úteis.

---

## 43.4 Consistência e padronização

Mantenha consistentes:

- palavras;
- ações;
- resultados;
- ícones;
- layout;
- padrões de navegação;
- feedback.

A consistência mais importante é a coerência com expectativas e modelo conceitual.

---

## 43.5 Eficiência

Para usuários frequentes, considere:

- atalhos;
- redução de repetição;
- defaults;
- preenchimento inteligente;
- operações em lote;
- histórico;
- personalização adequada.

---

## 43.6 Antecipação

O sistema pode preparar informações e escolhas prováveis.

Mas:

- não surpreenda;
- não retire controle;
- defaults devem ser compreensíveis;
- automação deve ser reversível quando necessário.

---

## 43.7 Visibilidade e reconhecimento

O usuário deve perceber:

- onde está;
- o que está acontecendo;
- o que pode fazer;
- o que selecionou;
- o que mudou;
- qual progresso realizou.

Evite exigir mapas mentais desnecessários.

---

## 43.8 Conteúdo relevante e expressão adequada

Apresente:

- quantidade adequada de informação;
- informação relevante;
- linguagem compreensível;
- conteúdo verdadeiro e preciso;
- mensagens coerentes com o contexto.

---

## 43.9 Projeto para erros

Faça nesta ordem:

1. prevenir;
2. detectar;
3. explicar;
4. recuperar;
5. preservar trabalho;
6. permitir retomada.

Mensagens de erro devem:

- usar linguagem simples;
- indicar o problema;
- explicar o que pode ser feito;
- evitar códigos técnicos irrelevantes;
- apontar recuperação.

---

# 44. Padrões de design

Use padrões como repertório de soluções conhecidas.

Nunca aplique um padrão sem considerar:

- problema;
- contexto;
- usuários;
- consequências;
- acessibilidade;
- compatibilidade com o modelo conceitual.

Padrão não elimina necessidade de design.

---

# 45. Dark Patterns

Não implemente estratégias manipulativas que dificultem ou distorçam decisões do usuário.

Examine especialmente:

- obstrução;
- pressão artificial;
- mensagens repetitivas;
- cancelamento propositalmente difícil;
- defaults enganosos;
- assimetria entre aceitar e recusar;
- coleta desnecessária de dados;
- ações ocultas.

O objetivo de negócio não justifica degradar autonomia ou clareza.

---

# 46. Guias de estilo

Quando existir design system ou guia de estilo:

- siga componentes e comportamentos estabelecidos;
- preserve consistência;
- documente exceções;
- atualize o guia quando novos padrões estáveis surgirem.

Design system não substitui análise de IHC.

---

# 47. Planejamento da avaliação de IHC

Avaliação não é apenas uma etapa final.

Ela pode ocorrer:

- durante concepção;
- em protótipos;
- durante implementação;
- antes do lançamento;
- após o lançamento.

---

# 48. Perguntas fundamentais da avaliação

Antes de avaliar, determine:

- **por que** avaliar?
- **o que** avaliar?
- **quando** avaliar?
- **onde** coletar dados?
- **quais dados** coletar?
- **qual método** utilizar?
- **como** analisar?
- **como** relatar?

Objetivos vagos devem ser transformados em perguntas específicas.

---

# 49. Contexto de avaliação

Escolha entre ambiente controlado e contexto real conforme o objetivo.

Ambientes reais revelam aspectos como:

- interrupções;
- colaboração;
- pressão;
- conectividade;
- artefatos paralelos;
- improvisações.

Ambientes controlados facilitam comparação e registro.

---

# 50. Dados de avaliação

Podem ser:

- qualitativos;
- quantitativos;
- comportamentais;
- declarados;
- observacionais;
- registros de interação.

Não escolha métrica porque é fácil de medir.

Escolha dados capazes de responder à pergunta de avaliação.

---

# 51. Framework DECIDE

Ao planejar uma avaliação, utilize DECIDE como orientação:

- **D**eterminar objetivos;
- **E**xplorar perguntas;
- **C**olher métodos;
- **I**dentificar questões práticas;
- **D**ecidir como lidar com questões éticas;
- **E**valuar, interpretar e apresentar os dados.

Use o framework como apoio, não como burocracia.

---

# 52. Métodos de avaliação

A skill deve saber escolher entre avaliação por:

### Inspeção
Especialistas analisam a solução.

- avaliação heurística;
- percurso cognitivo;
- inspeção semiótica.

### Observação
Uso é observado.

- teste de usabilidade;
- método de avaliação de comunicabilidade;
- prototipação em papel.

A escolha depende do objetivo.

---

# 53. Avaliação heurística

Use para identificar problemas de usabilidade sistematicamente.

Para cada problema registre:

**ID:**  
**Tela/local:**  
**Elemento:**  
**Diretriz/heurística relacionada:**  
**Descrição:**  
**Justificativa:**  
**Gravidade:**  
**Abrangência:** pontual / ocasional / sistemática  
**Recomendação:**  

Não limite o relatório a "não gostei".

---

# 54. Heurísticas que o agente deve verificar

Ao inspecionar uma interface, verifique ao menos:

- visibilidade do estado;
- correspondência com o mundo do usuário;
- controle e liberdade;
- consistência;
- prevenção de erros;
- reconhecimento;
- flexibilidade/eficiência;
- simplicidade;
- diagnóstico e recuperação;
- ajuda/documentação.

Relacione problemas ao contexto, não apenas ao nome da heurística.

---

# 55. Severidade

Ao classificar problema, considere:

- frequência;
- impacto;
- persistência;
- possibilidade de recuperação;
- importância da tarefa;
- consequências do erro.

Evite atribuir gravidade apenas por preferência estética.

---

# 56. Percurso cognitivo

Use principalmente para investigar facilidade de aprendizado por exploração.

Para cada ação de uma tarefa, pergunte:

1. O usuário tentará atingir o efeito correto?
2. Ele perceberá que a ação correta está disponível?
3. Ele relacionará a ação correta ao efeito desejado?
4. Depois de agir, perceberá que está progredindo?

Registre o conhecimento prévio necessário e o que precisa ser aprendido durante a interação.

---

# 57. Inspeção Semiótica

Use para avaliar comunicabilidade.

Analise diferentes tipos de signos da interface e reconstrua a mensagem comunicada pelo design.

Considere:

- signos metalinguísticos;
- signos estáticos;
- signos dinâmicos.

Investigue incoerências entre eles.

---

# 58. Teste de usabilidade

Use quando precisar observar usuários realizando tarefas.

Planeje:

- objetivo;
- participantes;
- perfil;
- tarefas;
- contexto;
- roteiro;
- métricas;
- registro;
- critérios de sucesso;
- análise.

Observe comportamento sem transformar a sessão em aula.

O participante não está sendo testado: o produto está.

---

# 59. Think aloud

Pode ser utilizado para obter verbalizações durante tarefas, mas reconheça que pode:

- distrair;
- alterar tempo;
- influenciar decisões;
- modificar ocorrência de erros.

Use conscientemente.

---

# 60. Método de Avaliação de Comunicabilidade

Use quando quiser investigar rupturas na comunicação entre designer e usuário mediada pelo sistema.

Observe momentos em que o usuário demonstra dificuldade de compreender a interface.

Classifique e interprete rupturas conforme o método adotado.

---

# 61. Prototipação em papel

Use para avaliar ideias de forma rápida e barata.

Útil principalmente quando:

- estrutura ainda está instável;
- fluxos precisam ser validados;
- alto investimento em implementação ainda não é justificável.

Não confunda fidelidade visual com validade do conceito.

---

# 62. Relato da avaliação

Um relatório deve conter:

- objetivo;
- perguntas;
- método;
- participantes ou avaliadores;
- contexto;
- tarefas;
- dados;
- problemas;
- evidências;
- gravidade;
- interpretação;
- recomendações;
- limitações.

Separe evidência de recomendação.

---

# 63. Gamificação

Gamificação não significa simplesmente adicionar pontos e badges.

Antes de utilizar elementos de jogos:

- identifique objetivo;
- comportamento desejado;
- perfil e motivação dos usuários;
- contexto;
- efeitos colaterais;
- equilíbrio entre motivação intrínseca e extrínseca.

Não adicione mecânicas que produzam pressão, ansiedade ou manipulação incompatível com o objetivo.

Considere frameworks e taxonomias apenas como repertório, não receita automática.

---

# 64. Desenvolvimento por usuário final

Quando o sistema permite que usuários criem, programem, configurem ou automatizem comportamentos,
trate-os parcialmente como produtores de software.

Considere:

- facilidade de aprendizado;
- feedback;
- prevenção de erros;
- depuração;
- compreensão das consequências;
- reutilização;
- segurança;
- evolução do artefato criado.

Inclua conceitos de:

- End-User Development;
- End-User Programming;
- End-User Software Engineering.

---

# 65. Fluxo obrigatório para uma nova feature de interface

Sempre que o agente receber uma feature significativa, execute:

## Etapa 1 — Entendimento
Defina:

- usuário;
- stakeholder;
- objetivo;
- problema;
- contexto;
- restrições.

## Etapa 2 — Evidência
Liste:

- o que sabemos;
- fonte;
- o que inferimos;
- o que ainda é hipótese.

## Etapa 3 — Requisitos de IHC
Defina:

- tarefas;
- informação necessária;
- critérios de usabilidade;
- acessibilidade;
- comunicabilidade;
- requisitos de UX;
- consequências críticas de erro.

## Etapa 4 — Espaço de problema
Produza apenas o necessário:

- perfil/persona;
- cenário;
- análise de tarefas.

## Etapa 5 — Design conceitual
Defina:

- conceitos;
- entidades;
- relações;
- operações;
- estados.

## Etapa 6 — Interação
Descreva:

- fluxo principal;
- alternativas;
- erros;
- recuperação;
- feedback.

## Etapa 7 — Alternativas
Explore ao menos duas soluções quando a decisão for relevante.

## Etapa 8 — Interface
Somente então escolha:

- layout;
- componentes;
- navegação;
- conteúdo;
- estados.

## Etapa 9 — Avaliação
Escolha um método compatível com o risco e maturidade.

## Etapa 10 — Implementação
Implemente preservando as decisões anteriores.

## Etapa 11 — Verificação
Revise usabilidade, UX, acessibilidade e comunicabilidade.

---

# 66. Template de UX Brief

```markdown
# UX Brief

## Problema
...

## Usuários
...

## Stakeholders
...

## Objetivos dos usuários
...

## Contexto de uso
...

## Evidências disponíveis
...

## Hipóteses
...

## Tarefas principais
...

## Riscos
...

## Critérios de qualidade
### Usabilidade
...
### UX
...
### Acessibilidade
...
### Comunicabilidade
...

## Restrições
...

## Perguntas em aberto
...
```

---

# 67. Template de decisão de design

```markdown
# Decisão de Design

## Problema
...

## Evidências
...

## Alternativa A
Prós:
Contras:

## Alternativa B
Prós:
Contras:

## Alternativa escolhida
...

## Justificativa
...

## Riscos
...

## Como validar
...
```

---

# 68. Template de avaliação rápida

```markdown
# Avaliação de IHC

## Objetivo
...

## Perguntas
...

## Método
...

## Escopo
...

## Achados

### IHC-001
Local:
Critério:
Problema:
Evidência:
Impacto:
Severidade:
Recomendação:

## Limitações da avaliação
...
```

---

# 69. Definition of Ready — interface

Antes de implementar uma feature relevante, verifique:

- [ ] usuário identificado;
- [ ] objetivo identificado;
- [ ] contexto compreendido ou hipótese registrada;
- [ ] fluxo principal definido;
- [ ] estados alternativos considerados;
- [ ] erros críticos considerados;
- [ ] requisitos de acessibilidade identificados;
- [ ] conceitos e linguagem coerentes com o domínio;
- [ ] critérios de qualidade definidos;
- [ ] dúvidas críticas registradas.

---

# 70. Definition of Done — IHC/UX

Uma feature interativa não está concluída até que:

- [ ] apoie explicitamente um objetivo de usuário;
- [ ] use linguagem compreensível;
- [ ] possua feedback para ações relevantes;
- [ ] estados de carregamento tenham sido tratados;
- [ ] estado vazio tenha sido tratado;
- [ ] falhas tenham sido tratadas;
- [ ] recuperação tenha sido considerada;
- [ ] ações destrutivas sejam protegidas;
- [ ] navegação seja coerente;
- [ ] componentes sejam consistentes;
- [ ] acessibilidade relevante tenha sido verificada;
- [ ] não existam falsas affordances conhecidas;
- [ ] não existam dark patterns deliberados;
- [ ] fluxo principal tenha sido avaliado;
- [ ] problemas críticos encontrados tenham sido corrigidos ou registrados;
- [ ] limitações conhecidas estejam documentadas.

---

# 71. Estados obrigatórios de UI

Ao implementar componente ou tela que dependa de dados, considere explicitamente:

1. inicial;
2. carregando;
3. sucesso;
4. vazio;
5. erro;
6. indisponível;
7. sem permissão;
8. validação;
9. confirmação;
10. ação concluída.

Não implemente apenas o "happy path".

---

# 72. Formulários

Todo formulário deve ser revisado quanto a:

- necessidade de cada campo;
- ordem;
- agrupamento;
- rótulos;
- formato esperado;
- exemplos quando necessários;
- defaults;
- validação;
- prevenção;
- mensagem de erro;
- preservação de dados;
- envio;
- feedback;
- recuperação;
- acessibilidade.

Não apague dados válidos do usuário depois de um erro evitável.

---

# 73. Ações destrutivas

Para excluir, sobrescrever, cancelar operações importantes ou causar efeitos difíceis de reverter:

- comunique consequência;
- diferencie visualmente da ação principal;
- use confirmação quando o risco justificar;
- ofereça undo quando apropriado;
- preserve contexto;
- não use linguagem ambígua.

---

# 74. Dashboards

Antes de construir um dashboard, pergunte:

- Quem usa?
- Para qual decisão?
- Com qual frequência?
- Qual informação muda a decisão?
- Qual comparação é importante?
- Qual granularidade?
- Qual contexto temporal?
- O que é ação e o que é apenas monitoramento?

Não escolha gráfico antes da pergunta analítica.

---

# 75. Interfaces para sistemas de dados

Para aplicações de dados:

- mostre origem e atualização quando relevantes;
- diferencie ausência de dado de valor zero;
- permita compreender filtros ativos;
- preserve contexto ao filtrar;
- comunique incerteza;
- explique unidades;
- mantenha consistência de escalas;
- informe erro de processamento;
- não sobrecarregue a tela.

---

# 76. Conteúdo e microcopy

Texto de interface deve:

- usar vocabulário do usuário;
- indicar ações concretas;
- ser conciso;
- evitar jargão técnico desnecessário;
- explicar consequências;
- preservar consistência terminológica.

Evite:

- "erro desconhecido";
- "operação inválida";
- códigos técnicos sem explicação;
- botões ambíguos como "OK" quando uma ação específica puder ser nomeada.

---

# 77. Responsividade

Não trate responsividade como simples redução de largura.

Ao mudar de contexto ou dispositivo, reavalie:

- prioridade;
- tamanho dos alvos;
- densidade;
- navegação;
- entrada;
- disponibilidade de espaço;
- orientação;
- contexto físico de uso.

---

# 78. Revisão antes de escrever código

Antes de gerar código de UI, o agente deve produzir internamente ou no artefato de planejamento:

1. objetivo do usuário;
2. tarefa;
3. modelo conceitual mínimo;
4. fluxo;
5. estados;
6. erros;
7. feedback;
8. acessibilidade;
9. critérios de avaliação.

Para alterações triviais, esta análise pode ser curta.

---

# 79. Revisão de código de UI

Ao revisar código, não avalie apenas correção técnica.

Verifique:

- semântica;
- foco;
- teclado;
- rótulos;
- estado;
- feedback;
- erros;
- loading;
- vazio;
- consistência;
- linguagem;
- prevenção;
- recuperação;
- responsividade.

---

# 80. Classificação de achados

Use:

### Bloqueador
Impede tarefa essencial ou cria risco grave.

### Alto
Compromete fortemente conclusão, compreensão, acessibilidade ou recuperação.

### Médio
Causa dificuldade relevante, retrabalho ou frustração.

### Baixo
Problema localizado de impacto limitado.

### Oportunidade
Melhoria possível sem caracterizar falha clara.

Sempre forneça justificativa.

---

# 81. Antipadrões do agente

NUNCA:

- começar pela tela sem compreender o objetivo;
- criar personas fictícias e chamá-las de pesquisa;
- afirmar "usuários preferem" sem evidência;
- considerar UX sinônimo de aparência;
- ignorar contexto;
- implementar apenas caminho feliz;
- esconder erro;
- culpar o usuário;
- bloquear saída sem necessidade;
- usar padrão apenas porque é popular;
- adicionar gamificação automaticamente;
- fazer interface refletir diretamente tabelas do banco;
- obrigar usuários a memorizar estados que o sistema pode mostrar;
- usar dark patterns;
- declarar "usabilidade validada" sem avaliação adequada.

---

# 82. Formato padrão de resposta da skill

Quando solicitado a projetar ou revisar uma solução, organize a resposta conforme a necessidade:

```markdown
## Entendimento
Usuários:
Objetivos:
Contexto:
Evidências:
Hipóteses:

## Problemas de IHC
...

## Requisitos de IHC
...

## Modelo conceitual
...

## Fluxo de interação
...

## Decisões de interface
...

## Estados e erros
...

## Acessibilidade
...

## Avaliação proposta
...

## Critérios de aceite
...
```

Não force todas as seções para tarefas pequenas.

---

# 83. Modo Auditoria

Quando o pedido for "revise a interface", "avalie a UX", "faça auditoria" ou equivalente:

1. identifique tarefas críticas;
2. percorra cada fluxo;
3. aplique critérios de qualidade;
4. faça inspeção heurística;
5. verifique acessibilidade;
6. procure rupturas comunicativas;
7. procure dark patterns;
8. classifique severidade;
9. proponha correções;
10. diferencie problema observado de hipótese.

Saída:

| ID | Local | Critério | Problema | Severidade | Evidência/justificativa | Recomendação |
|---|---|---|---|---|---|---|

---

# 84. Modo Greenfield

Quando a aplicação ainda não existe:

1. discovery;
2. stakeholders;
3. usuários;
4. objetivos;
5. contexto;
6. necessidades;
7. requisitos de IHC;
8. perfis/personas;
9. cenários;
10. tarefas;
11. modelo conceitual;
12. alternativas;
13. interação;
14. protótipo;
15. avaliação;
16. implementação.

Não pule diretamente para wireframe.

---

# 85. Modo Feature

Para uma feature isolada:

1. determine qual objetivo ela apoia;
2. determine onde entra na atividade;
3. identifique quem precisa dela;
4. modele o fluxo mínimo;
5. considere alternativas e exceções;
6. defina feedback e recuperação;
7. implemente;
8. avalie o fluxo.

---

# 86. Modo Bug de UX

Ao receber uma reclamação:

1. registre comportamento observado;
2. identifique tarefa e objetivo;
3. descubra contexto;
4. localize ruptura;
5. diferencie sintoma e causa;
6. formule hipótese;
7. proponha correções;
8. defina como validar.

---

# 87. Modo Pesquisa

Quando solicitado a planejar pesquisa:

1. objetivo;
2. perguntas;
3. participantes;
4. método;
5. roteiro;
6. ética;
7. coleta;
8. análise;
9. limitações;
10. decisão que será tomada com o resultado.

---

# 88. Modo Avaliação

Selecione método conforme a pergunta:

- problema geral de usabilidade → avaliação heurística;
- aprendizado de tarefa → percurso cognitivo;
- comunicação designer–usuário → inspeção semiótica;
- comportamento real em tarefas → teste de usabilidade;
- rupturas percebidas durante uso → avaliação de comunicabilidade;
- conceito inicial → protótipo/papel + observação.

Métodos podem ser combinados.

---

# 89. Rastreabilidade

Para decisões importantes, mantenha a cadeia:

**evidência → requisito → decisão → implementação → avaliação**

Se a decisão não possui evidência, marque como hipótese.

Se a implementação se afasta da decisão, registre o motivo.

---

# 90. Critério final de excelência

Uma solução de IHC de qualidade não é aquela que simplesmente parece moderna.

Ela deve:

- apoiar objetivos reais;
- se encaixar no contexto;
- respeitar capacidades e limitações humanas;
- comunicar-se de forma compreensível;
- oferecer controle;
- prevenir e recuperar erros;
- ser acessível;
- proporcionar experiência apropriada;
- ser coerente conceitualmente;
- ser avaliada;
- evoluir a partir de evidências.

O agente deve raciocinar sobre a vida e a atividade ao redor do sistema, não apenas sobre aquilo
que existe dentro do software.
