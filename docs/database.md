# Modelo de dados — MongoDB Atlas

## Escopo atual

O MVP utiliza `users`, `subjects` e `study_sessions`. O schema abaixo descreve a persistência vigente e as decisões de isolamento aplicadas pelos repositories.

## Collections

### `users`

Finalidade: identidade mínima do usuário e meta semanal.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `_id` | ObjectId | sim |
| `name` | string | sim |
| `email` | string | sim |
| `identity.provider` | string | sim para usuários autenticados |
| `identity.subject` | string | sim para usuários autenticados |
| `weekly_goal_minutes` | integer | sim |
| `current_academic_period_id` | ObjectId | não |

Identidade única: `{identity.provider: 1, identity.subject: 1}` unique e parcial. O e-mail é atributo de perfil, não chave de identidade, e não possui unicidade global. Crescimento: um documento por usuário.

`current_academic_period_id` referencia um período ativo pertencente ao usuário. A referência fica no usuário porque existe apenas um contexto atual por vez e a troca é uma escrita pequena e frequente.

### `academic_periods`

Finalidade: representar semestres ou ciclos acadêmicos do usuário sem misturá-los a disciplinas ou sessões.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `_id` | ObjectId | sim |
| `user_id` | ObjectId | sim |
| `name` | string | sim |
| `name_normalized` | string | sim |
| `start_date` | string ISO `YYYY-MM-DD` | sim |
| `end_date` | string ISO `YYYY-MM-DD` | sim |
| `status` | enum `ACTIVE`/`ARCHIVED` | sim |
| `created_at` | BSON datetime UTC | sim |
| `updated_at` | BSON datetime UTC | sim |

Cardinalidade: um usuário possui vários períodos; um período pertence a um usuário e pode ser referenciado por várias disciplinas. A collection é referenciada, não embutida, porque períodos possuem ciclo de vida próprio.

Índices:

- `{user_id: 1, name_normalized: 1}` unique parcial: impede nomes equivalentes no mesmo usuário e permite nomes iguais entre usuários;
- `{user_id: 1, status: 1, start_date: -1}`: apoia listagem dos períodos ativos/arquivados em ordem temporal.

Leituras: listar períodos do usuário, verificar nome duplicado e validar que o período selecionado está ativo e pertence ao usuário. Escritas: criar, definir como atual por referência em `users` e arquivar sem excluir o histórico.

### `subjects`

Finalidade: disciplinas pertencentes a um usuário.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `_id` | ObjectId | sim |
| `user_id` | ObjectId | sim |
| `academic_period_id` | ObjectId | sim para novos documentos |
| `name` | string | sim |
| `name_normalized` | string | sim para novos documentos |
| `color` | string hexadecimal | sim |

Relacionamento por referência a `users` e `academic_periods`; embedding não é adequado porque disciplinas são alteradas e consultadas separadamente. O índice `{user_id: 1, academic_period_id: 1, name: 1}` apoia a listagem do período. O índice parcial unique `{user_id: 1, academic_period_id: 1, name_normalized: 1}` permite repetir uma disciplina em semestres diferentes e impede duplicatas dentro do mesmo período. Documentos legados sem `academic_period_id` ficam fora do índice parcial e são listados explicitamente como “Sem período”.

### `study_sessions`

Finalidade: planejamento e acompanhamento de sessões.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `_id` | ObjectId | sim |
| `user_id` | ObjectId | sim |
| `academic_period_id` | ObjectId | sim para novas sessões |
| `subject_id` | ObjectId | sim |
| `topic` | string | sim |
| `study_date` | string ISO `YYYY-MM-DD` (atual) | sim |
| `study_time` | string `HH:MM` (atual) | sim |
| `duration` | integer minutos | sim |
| `priority` | enum string | sim |
| `status` | enum string | sim |
| `goal` | string | não |

Relaciona-se por referência a `users`, `academic_periods` e `subjects`. Não embutir sessões em usuário ou disciplina: o array cresce e sessões são consultadas/atualizadas individualmente. Índice atual `{user_id: 1, study_date: 1, study_time: 1}` apoia agenda e checagem de conflito. Sessões legadas continuam legíveis por `subject_id`; novas sessões registram também o período atual.

## Consultas esperadas

- Buscar o usuário ativo por `identity.provider + identity.subject`.
- Listar disciplinas por `user_id + academic_period_id`, ordenadas por nome.
- Listar separadamente disciplinas legadas sem `academic_period_id`.
- Listar períodos acadêmicos por `user_id`, status e data inicial.
- Listar sessões de um usuário por intervalo de datas e horário.
- Buscar sessões pendentes de uma data para validar sobreposição.
- Agregar minutos concluídos por semana e disciplina.

## Escritas esperadas

Criar/arquivar período e selecionar o atual; criar/editar/excluir disciplina; criar/editar/reagendar/concluir/excluir sessão; atualizar a meta semanal. Todas devem filtrar pelo usuário autorizado e validar referências.

## Pendências

- Escolher se datas/horários passam para BSON `date` ou permanecem strings ISO; BSON é preferível quando consultas temporais crescerem.
- Definir política de migração dos documentos legados sem `identity` ou `name_normalized`.
- Definir um fluxo explícito para o usuário associar disciplinas legadas a períodos; nenhuma relação é inferida automaticamente.
- Adicionar validação de schema e índices finais na camada de infraestrutura.
