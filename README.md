# HybridSort

Interface visual para explorar uma lista híbrida, com busca binária na região
ordenada e busca sequencial na cauda.

## Executar

Instale o projeto e suas dependências:

```powershell
python -m pip install -e .
```

Inicie a interface:

```powershell
hybridsort
```

Também é possível iniciar o app diretamente com Streamlit:

```powershell
python -m streamlit run src/hybridsort/app.py
```

Na interface, é possível buscar e inserir chaves, reiniciar a lista com uma
semente escolhida e visualizar os índices, as regiões e as iterações usadas.

## Publicar no Streamlit Community Cloud

O repositório contém a dependência de execução em `requirements.txt` e usa
Python 3.12, definido em `.python-version`. Para criar a publicação:

1. Abra o [Streamlit Community Cloud](https://share.streamlit.io/) e conecte a
   conta do GitHub que tem acesso ao repositório.
2. Crie um app selecionando o repositório `DrewGDev/hybridsort` e a branch
   `main`.
3. Informe `src/hybridsort/app.py` como arquivo principal e selecione Python
   3.12 nas configurações avançadas.
4. Publique o app. O Cloud mostrará o endereço público `*.streamlit.app` ao
   terminar a implantação.

O Streamlit Community Cloud exige permissão administrativa no repositório para
conectar e implantar o app. Consulte a documentação oficial de
[implantação](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
e de [permissões do GitHub](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account).
