# Plano — planejador de estudos

Protótipo de um planejador de estudos feito com Streamlit e SQLite. O banco é criado automaticamente na primeira execução e recebe um usuário de teste com disciplinas e sessões de exemplo.

## Regras atuais

- sessões só podem ser planejadas para hoje ou uma data futura;
- sessões pendentes com data passada aparecem como atrasadas;
- horários de sessões pendentes não podem se sobrepor;
- a visão geral acompanha a meta semanal em horas;
- a página de progresso resume o tempo concluído por disciplina;
- o banco possui uma migração simples para manter instalações anteriores funcionando.

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

## Rodar no Google Colab com dados persistentes

Monte o Google Drive antes de iniciar o app:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Se a pasta `/content/drive/MyDrive/IhcStreamlitApp` existir, o app salva automaticamente o banco em `estudos.db` dentro dela. Caso contrário, ele usa um banco local temporário.

Para usar o fluxo do notebook original, instale o Streamlit e exponha a porta 8501 com Localtunnel. O endereço público é temporário.
