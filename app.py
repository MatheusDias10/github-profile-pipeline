"""
Fazendo a interface web rodar com todo o prrocesso ETL embutido.
"""

import os
import pandas as pd
import streamlit as st

from pandas.errors import EmptyDataError
from etl_process.extract.extract_github_client import busca_usuario
from etl_process.transform.transform_data import ajustar_dados
from etl_process.load.perfil_load import salva_log, salva_unique


LOG_CSV = "data/log.csv"
USERS_CSV = "data/users.csv"

# Titulo da página.
st.title("GitHub Profile Viewer")
st.write("Exibição dos dados públicos de um perfil do GitHub")

# Criando o input aonde será feito a extração do usuário
username = st.text_input("Digite o nome do usuário GitHub: ")

# Criando os botões
if st.button("Buscar"):
    raw = busca_usuario(username)
    if raw is None:
        st.error("Falha na extração. Verifique o usuário e tente novamente.")
    else:
        # Limpando os dados do df "raw" que recebeu os dados do usuario
        clean = ajustar_dados(raw)
        st.success("Dados carregados com sucesso.")
        st.dataframe(clean)

        # Atualiza log completo
        salva_log(clean, LOG_CSV)
        # Atualiza a lista única
        salva_unique(clean, USERS_CSV)

        st.info(f"Perfil adicionado ao log: {LOG_CSV}")
        st.info(f"Lista única atualizada: {USERS_CSV}")

# Botão para ver o log
if st.button("Ver histórico"):
    df_log = pd.read_csv(LOG_CSV, parse_dates=["created_at", "updated_at"])
    st.dataframe(df_log)

# Botão para ver os usuários únicos
if st.button("Ver usuários únicos"):
    # Fazendo uma precaução para caso o arquivo esteja vazio ou não exista
    if not os.path.exists(USERS_CSV) or os.path.getsize(USERS_CSV) == 0:
        st.warning("Ainda não há usuários únicos salvos. Clique em Buscar para gerar o arquivo.")
    else:
        # Passando o df users.csv no botão de "ver usuários únicos"
        try:
            df_users = pd.read_csv(
                USERS_CSV, parse_dates=["created_at", "updated_at"]
            )
            st.dataframe(df_users)
        except EmptyDataError:
            st.warning("O arquivo de usuários está vazio.")

# Criando um botão de limpar os dados das tabelas.
if st.button("Limpar dados da tabela"):
    # Se ambas pastas existirem faça isso:
    if os.path.exists(USERS_CSV) and os.path.exists(LOG_CSV):
        # Recriando os arquivos para aparecerem apenas com a linha de cabeçalho
        df_header = pd.read_csv(USERS_CSV, nrows=0)
        df_header = df_header.to_csv(USERS_CSV, index=False)
        
        df_header2 = pd.read_csv(LOG_CSV, nrows=0)
        df_header2 = df_header2.to_csv(LOG_CSV, index=False)
        
        st.success("O histórico foi limpo.")
    else:
        st.warning("Este arquivo não existe.")
