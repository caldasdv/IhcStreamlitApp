# Modelo de dados — MongoDB Atlas

## Escopo da Sprint 0

Os requisitos disponíveis permitem identificar os conceitos `users`, `subjects` e `study_sessions`, já usados pelo protótipo. O schema abaixo é conceitual e deve ser consolidado antes da extração dos repositories. Não há entidades adicionais inventadas.

## Collections

### `users`

Finalidade: identidade mínima do usuário e meta semanal.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `_id` | ObjectId | sim |
| `name` | string | sim |
| `email` | string | sim |
| `weekly_goal_minutes` | integer | sim |

Índice: `{email: 1}` unique, para identidade única. Crescimento: um documento por usuário.

### `subjects`

Finalidade: disciplinas pertencentes a um usuário.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `_id` | ObjectId | sim |
| `user_id` | ObjectId | sim |
| `name` | string | sim |
| `color` | string hexadecimal | sim |

Relacionamento por referência a `users`; embedding não é adequado porque disciplinas são alteradas e consultadas separadamente. Índice atual `{user_id: 1, name: 1}`; avaliar unicidade por usuário na implementação de criação.

### `study_sessions`

Finalidade: planejamento e acompanhamento de sessões.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `_id` | ObjectId | sim |
| `user_id` | ObjectId | sim |
| `subject_id` | ObjectId | sim |
| `topic` | string | sim |
| `study_date` | string ISO `YYYY-MM-DD` (atual) | sim |
| `study_time` | string `HH:MM` (atual) | sim |
| `duration` | integer minutos | sim |
| `priority` | enum string | sim |
| `status` | enum string | sim |
| `goal` | string | não |

Relaciona-se por referência a `users` e `subjects`. Não embutir sessões em usuário ou disciplina: o array cresce e sessões são consultadas/atualizadas individualmente. Índice atual `{user_id: 1, study_date: 1, study_time: 1}` apoia agenda e checagem de conflito.

## Consultas esperadas

- Buscar o usuário ativo por `_id`/email.
- Listar disciplinas por `user_id`, ordenadas por nome.
- Listar sessões de um usuário por data e horário.
- Buscar sessões pendentes de uma data para validar sobreposição.
- Agregar minutos concluídos por semana e disciplina.

## Escritas esperadas

Criar/editar/excluir disciplina; criar/editar/reagendar/concluir/excluir sessão; atualizar a meta semanal. Todas devem filtrar pelo usuário autorizado e validar referências.

## Pendências

- Definir autenticação/seleção de usuário antes de produção.
- Escolher se datas/horários passam para BSON `date` ou permanecem strings ISO; BSON é preferível quando consultas temporais crescerem.
- Definir política de seed e migrações.
- Adicionar validação de schema e índices finais na camada de infraestrutura.
