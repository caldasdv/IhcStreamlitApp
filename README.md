# Plano — planejador de estudos

Protótipo de um planejador de estudos feito com Streamlit e MongoDB Atlas. O banco é preparado automaticamente na primeira execução e recebe um usuário de teste com disciplinas e sessões de exemplo.

## Regras atuais

- sessões só podem ser planejadas para hoje ou uma data futura;
- sessões pendentes com data passada aparecem como atrasadas;
- horários de sessões pendentes não podem se sobrepor;
- a visão geral acompanha a meta semanal em horas;
- a página de progresso resume o tempo concluído por disciplina;
- a conexão usa `MONGODB_URI` e o banco `plano_estudos` no Atlas.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Variáveis de ambiente

As credenciais locais ficam no arquivo `.env`, que não é versionado. Para configurar:

```bash
cp .env.example .env
```

Depois substitua `<db_password>` pela senha do usuário criado no MongoDB Atlas. A URI está disponível para a próxima etapa de migração do SQLite para o Atlas.

## Rodar em uma VPS ou no Community Cloud

Configure `MONGODB_URI` nas variáveis de ambiente da VPS ou nos Secrets do Community Cloud. O app não depende mais de SQLite ou Google Drive.
