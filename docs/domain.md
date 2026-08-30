# Domínio do Plano

## Propósito

O produto apoia o ciclo:

```text
PLANEJAR → AGENDAR → ESTUDAR → REGISTRAR → ANALISAR → REPLANEJAR
```

Este documento organiza conceitos atuais e planejados. Uma entidade marcada como planejada não autoriza automaticamente collection, página ou dependência nova; ela precisa de User Story pronta, modelo de dados aprovado e critérios de aceite.

## Mapa conceitual

```text
User
├── AcademicPeriod
│   └── Subject
│       ├── ClassMeeting
│       ├── Topic
│       ├── Material
│       └── Grade
├── Task ── SubTask
├── Exam ── ExamTopic
├── StudySession ── FocusSession
├── Availability
├── Goal / Habit / Reminder
└── CalendarEvent
```

Tarefa, prova, aula, sessão de estudo e evento não são sinônimos. Uma camada de apresentação pode reuni-los no calendário, mas não deve apagar suas diferenças de negócio.

## Entidades implementadas

### User

Representa a conta autenticada. A identidade estável é `provider + subject`; e-mail é atributo de perfil. Toda entidade privada pertence a um usuário e toda operação por ID repete o filtro de `user_id`.

Responsabilidades atuais: nome, e-mail, identidade OIDC, meta semanal e referência ao período acadêmico atual.

### AcademicPeriod

Representa semestre ou ciclo acadêmico com nome, início, fim e estado.

Estados:

```text
ACTIVE | ARCHIVED
```

Invariantes:

- nome não vazio e único por usuário após normalização;
- fim igual ou posterior ao início;
- primeiro período criado torna-se atual;
- período atual deve estar ativo e pertencer ao usuário;
- período atual não pode ser arquivado até outro ser escolhido;
- arquivar preserva histórico.

### Subject

Representa disciplina pertencente ao usuário.

Invariantes atuais:

- nome não vazio e único por usuário após normalização;
- cor hexadecimal válida;
- uma sessão só pode referenciar disciplina pertencente ao mesmo usuário.

Próxima decisão: associar disciplina ao período acadêmico atual e tratar documentos legados sem inferir vínculo incorreto.

### StudySession

Representa um bloco planejado de estudo, não uma tarefa nem execução de cronômetro.

Estados atuais:

```text
Pendente | Concluída
```

`Atrasada` é um estado efetivo de apresentação para sessão pendente em data passada.

Invariantes:

- assunto obrigatório;
- planejamento apenas para hoje ou futuro;
- duração positiva;
- sessões pendentes do mesmo usuário não se sobrepõem no mesmo dia;
- conclusão, alteração e exclusão filtram por sessão e usuário;
- prazo de tarefa futuro não deve ser confundido com horário da sessão.

## Entidades planejadas

| Entidade | Finalidade | Prioridade indicativa | Dependências |
|---|---|---:|---|
| ClassMeeting | aula recorrente de uma disciplina | P0/P1 | período + disciplina |
| Topic | conteúdo e progresso dentro da disciplina | P1 | disciplina |
| Task/SubTask | entrega com prazo e progresso parcial | P1 | disciplina/período |
| Exam/ExamTopic | prova e conteúdos cobrados | P1 | disciplina + tópicos |
| FocusSession | execução real de uma sessão planejada | P1 | StudySession |
| Material | link ou referência de estudo | P1 | disciplina/tópico |
| Availability | janelas semanais disponíveis | P1 | usuário/timezone |
| Goal | meta mensurável por período | P1 | métricas confiáveis |
| Grade | resultado acadêmico | P1/P2 | disciplina/prova |
| Reminder | lembrete associado a entidade | P1/P2 | estratégia de notificações |
| Habit | comportamento recorrente distinto de tarefa | P2 | regras próprias |
| CalendarEvent | evento pessoal que bloqueia agenda | P1/P2 | calendário unificado |

## Calendário

O calendário normaliza itens para exibição sem persistir tudo em uma collection genérica:

```text
CLASS | EXAM | TASK_DEADLINE | STUDY_SESSION | EVENT
```

Cada item preserva `source_id` e `type`, e ações retornam à entidade de origem. Drag-and-drop e redimensionamento exigem validação de conflitos, autorização e fallback acessível antes de implementação.

## Escopo excluído no momento

Não implementar sem nova decisão: chat com IA/LLM, geração automática de resumos ou flashcards, OCR, rede social, grupos, marketplace, videoconferência ou gamificação complexa. Planejamento inteligente deve começar por regras, heurísticas, scoring explicável e dados do próprio usuário.
