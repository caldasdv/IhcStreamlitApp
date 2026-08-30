# Plano — planejador de estudos

Protótipo de um planejador de estudos feito com Streamlit e SQLite. O banco é criado automaticamente na primeira execução e recebe um usuário de teste com disciplinas e sessões de exemplo.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Rodar no Google Colab com dados persistentes

Monte o Google Drive antes de iniciar o app:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Se a pasta `/content/drive/MyDrive/IhcStreamlitApp` existir, o app salva automaticamente o banco em `estudos.db` dentro dela. Caso contrário, ele usa um banco local temporário.

Para usar o fluxo do notebook original, instale o Streamlit e exponha a porta 8501 com Localtunnel. O endereço público é temporário.
