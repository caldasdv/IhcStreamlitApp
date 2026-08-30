# Plano — planejador de estudos

Aplicação web para estudantes organizarem períodos acadêmicos, disciplinas, grade de aulas e sessões de estudo, acompanhando o progresso semanal com dados persistidos no MongoDB Atlas.

Aplicação publicada: [planejadordeestudos.streamlit.app](https://planejadordeestudos.streamlit.app/)

## Estado atual

O MVP está operacional e as entregas funcionais até a Sprint 17 foram integradas. A avaliação de usabilidade da Sprint 12 possui protocolo pronto, mas ainda depende de participantes e não deve ser considerada concluída.

Principais fluxos:

- login com Google OIDC;
- isolamento dos dados por usuário autenticado;
- criação, seleção e arquivamento de períodos acadêmicos;
- disciplinas vinculadas ao período atual;
- associação manual de disciplinas legadas a períodos ativos;
- grade semanal de aulas com detecção de conflitos;
- criação, edição, conclusão e exclusão de sessões de estudo;
- agenda semanal, meta de horas e dashboard de progresso;
- feedback persistente após reruns e estados de erro recuperáveis.

## Stack

- Python 3.11–3.14;
- Streamlit com suporte a autenticação OIDC;
- MongoDB Atlas e PyMongo;
- Plotly para visualizações analíticas justificadas;
- pytest para testes automatizados;
- Streamlit Community Cloud para deploy.

Pandas não é dependência atual e só deve ser adicionada quando houver necessidade concreta.

## Arquitetura

O projeto usa um monólito modular:

```text
Streamlit UI / Pages
        ↓
Application Services
        ↓
Domain + Repository contracts
        ↓
MongoDB repositories
        ↓
MongoDB Atlas
```

As páginas não acessam MongoDB diretamente. Regras de negócio ficam fora do Streamlit e podem ser testadas sem iniciar a aplicação. O `MongoClient` e os services são recursos compartilhados com `st.cache_resource`.

Comece pelo [índice da documentação](docs/README.md). As fontes principais são [arquitetura](docs/architecture.md), [domínio](docs/domain.md), [banco](docs/database.md) e [backlog](docs/backlog.md).

Para auditorias de segurança, use a skill repo-local em [`skills/security-audit/SKILL.md`](skills/security-audit/SKILL.md). Ela define a descoberta da stack, a matriz de evidências e a geração validada do relatório PDF.

O roadmap de evolução visual e componentes externos está em [docs/frontend-roadmap.md](docs/frontend-roadmap.md).

## Estrutura

- `app.py`: entrypoint fino usado pelo Community Cloud.
- `app_pages/`: scripts das páginas registradas por `st.navigation`, incluindo períodos e grade de aulas.
- `src/ui/`: contexto, sidebar, estilos e componentes reutilizáveis.
- `src/services/`: casos de uso sem dependência direta da UI.
- `src/repositories/`: contratos e adapters MongoDB.
- `src/domain/`: regras testáveis sem Streamlit.
- `tests/`: testes unitários de domínio, services e repositories sem Atlas.
- A tela `Progresso` inclui métricas semanais e visualizações Plotly por disciplina e por dia, com tabela textual equivalente.

O shell real está em `src/ui/app_shell.py`. Tanto `app.py` quanto o entrypoint de compatibilidade `src/app.py` executam esse mesmo shell.

## Regras atuais

- sessões só podem ser planejadas para hoje ou uma data futura;
- sessões pendentes com data passada aparecem como atrasadas;
- horários de sessões pendentes não podem se sobrepor;
- a visão geral acompanha a meta semanal em horas;
- a página de progresso resume o tempo concluído por disciplina;
- a conexão usa `MONGODB_URI` e o banco `plano_estudos` no Atlas.
- o primeiro período acadêmico criado vira o atual; períodos não atuais podem ser arquivados sem apagar o histórico.
- disciplinas novas pertencem ao período atual; registros antigos sem período continuam preservados e identificados.
- disciplinas antigas podem ser associadas manualmente a um período ativo, sem alterar suas sessões existentes.
- a grade semanal registra aulas recorrentes por disciplina e rejeita sobreposição de horários.

## Preparar o ambiente local

Na raiz do repositório:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
```

No Windows PowerShell, a ativação equivalente é:

```powershell
.venv\Scripts\Activate.ps1
```

## MongoDB Atlas

Crie um cluster, um usuário de banco com privilégios mínimos necessários e uma regra de rede compatível com o ambiente de execução. Nunca use a conta administrativa do Atlas na aplicação.

Para desenvolvimento local, crie `.env` na raiz:

```dotenv
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER/?retryWrites=true&w=majority
MONGODB_DATABASE=plano_estudos
```

O `.env` é ignorado pelo Git. Não coloque credenciais no código, README, issues, commits ou logs.

## Login Google local

1. No Google Cloud Console, configure a tela de consentimento OAuth.
2. Crie um cliente OAuth 2.0 do tipo aplicação web.
3. Registre exatamente `http://localhost:8501/oauth2callback` em **URIs de redirecionamento autorizados**.
4. Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml`.
5. Preencha o bloco `[auth]` com os dados do cliente local e gere um `cookie_secret` longo e aleatório.

Exemplo local completo:

```toml
[mongodb]
uri = "mongodb+srv://USERNAME:PASSWORD@CLUSTER/?retryWrites=true&w=majority"
database = "plano_estudos"

[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "GENERATE_A_LONG_RANDOM_SECRET"
client_id = "GOOGLE_CLIENT_ID"
client_secret = "GOOGLE_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

O arquivo `.streamlit/secrets.toml` é ignorado e nunca deve ser commitado. A identidade interna usa `provider + sub` do Google; e-mail é somente atributo de perfil.

## Executar e testar

Com o ambiente ativado:

```bash
python -m streamlit run app.py
```

A aplicação local usa normalmente `http://localhost:8501`.

Validação completa:

```bash
python -m pytest -q
python -m compileall -q app.py app_pages src tests
python -m pip check
```

Os testes unitários não exigem conexão com Atlas nem credenciais. O smoke test manual exige a configuração de autenticação correspondente ao endereço usado.

## Deploy no Streamlit Community Cloud

1. Publique a branch desejada no GitHub.
2. No Community Cloud, selecione o repositório, a branch e `app.py` como entrypoint.
3. Em **App settings → Secrets**, informe um TOML completo; não cole no formato `.env`.
4. No cliente OAuth do Google, registre exatamente a URL pública terminada em `/oauth2callback`.
5. Garanta que o MongoDB Atlas aceite conexões originadas pelo ambiente do Community Cloud.
6. Reinicie o app e valide login, criação de período, disciplina, grade e sessão.

Secrets para a aplicação publicada:

```toml
[mongodb]
uri = "mongodb+srv://USERNAME:PASSWORD@CLUSTER/?retryWrites=true&w=majority"
database = "plano_estudos"

[auth]
redirect_uri = "https://planejadordeestudos.streamlit.app/oauth2callback"
cookie_secret = "GENERATE_A_DIFFERENT_LONG_RANDOM_SECRET"
client_id = "GOOGLE_CLIENT_ID"
client_secret = "GOOGLE_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

Alternativamente, a URI pode ser fornecida como Secret de topo `MONGODB_URI` e o banco como `MONGODB_DATABASE`, mas o formato `[mongodb]` acima é o padrão documentado do projeto.

O app não usa SQLite, Google Drive nem arquivos locais como armazenamento persistente.

## Segurança operacional

- rotacione imediatamente qualquer credencial publicada ou enviada para commits;
- use usuários Atlas dedicados e privilégios mínimos;
- mantenha `.env` e `.streamlit/secrets.toml` fora do Git;
- não imprima URI, tokens, senhas ou claims desnecessários;
- revise o histórico Git quando houver suspeita de vazamento;
- toda operação privada deve continuar filtrando `user_id` e, quando aplicável, período e entidade relacionada.

## Contribuição

Leia [AGENTS.md](AGENTS.md) antes de alterar o projeto. Use uma branch curta por sprint ou entrega, atualize testes e documentação no mesmo trabalho e abra Pull Request para `main`. O fluxo detalhado está em [docs/git-workflow.md](docs/git-workflow.md).
