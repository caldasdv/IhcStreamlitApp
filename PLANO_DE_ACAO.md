# Plano de ação — Plano

## Objetivo

Construir um planejador de estudos simples, confiável e agradável de usar, aplicando princípios de IHC no próprio fluxo do produto. A aplicação será feita em Streamlit, publicada pelo Community Cloud ou VPS e terá o MongoDB Atlas como persistência.

## Decisões já tomadas

- Streamlit como camada de interface.
- MongoDB Atlas como banco de dados.
- `pymongo` como driver Python; Mongoose não será usado.
- Segredos fora do Git, usando `st.secrets` no Community Cloud e variáveis de ambiente na VPS.
- Projeto sem notebook do Colab e sem Localtunnel.
- Interface com inspiração no Notion: limpa, clara, com poucos efeitos e foco no conteúdo.
- Componentes nativos do Streamlit sempre que possível.

## Estado atual

- [x] Usuário de teste e dados iniciais.
- [x] Cadastro de disciplinas e sessões.
- [x] Meta semanal e acompanhamento por disciplina.
- [x] Regras de conflito de horário e sessões atrasadas.
- [x] Persistência migrada de SQLite para MongoDB Atlas.
- [x] Estrutura organizada em `src/`.
- [x] Notebook do Colab removido.
- [x] Deploy compatível com `app.py` na raiz e `src/app.py`.
- [x] Validar leitura dos Secrets no Community Cloud.
- [x] Criar índices básicos no MongoDB para as consultas do planejador.
- [ ] Melhorar a separação entre interface, regras e acesso ao banco.
- [ ] Adicionar edição e reagendamento de sessões.
- [ ] Adicionar visão semanal com ações rápidas.
- [ ] Adicionar autenticação ou seleção real de usuário.
- [ ] Criar testes automatizados das regras de negócio.
- [ ] Revisar acessibilidade, textos e estados vazios.

## Ordem de desenvolvimento

### 1. Fundação e segurança

- Usar `st.secrets` no Community Cloud e `MONGODB_URI` na VPS.
- Manter `.env`, `.venv`, secrets locais e skills fora do Git.
- Criar índices no Atlas para usuário, data e disciplina.
- Tratar falhas de conexão com uma mensagem útil e sem expor credenciais.

### 2. Domínio do planejador

- Centralizar as regras de sessão em funções testáveis.
- Definir estados: pendente, concluída e atrasada.
- Impedir conflitos de horário e sessões inválidas.
- Permitir editar, reagendar, concluir e excluir com confirmação.

### 3. Fluxos principais

- Visão geral: foco no dia atual e nas próximas sessões.
- Nova sessão: formulário curto, objetivo claro e validação imediata.
- Calendário semanal: leitura rápida da carga de estudos.
- Progresso: tempo concluído, meta e distribuição por disciplina.

### 4. IHC e visual

- Manter hierarquia visual inspirada no Notion.
- Preferir componentes nativos, sentence case e ícones Material Symbols.
- Evitar sombras, gradientes e excesso de cards.
- Usar feedback, prevenção de erros, estados vazios e mensagens claras.
- Validar o fluxo com tarefas reais de estudantes.

### 5. Qualidade e entrega

- Rodar validação de sintaxe e testes das regras.
- Testar localmente com MongoDB Atlas.
- Verificar os logs do Community Cloud após cada deploy.
- Atualizar o README e commitar cada etapa coerente.
