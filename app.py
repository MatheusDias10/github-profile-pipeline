import streamlit as st
import pandas as pd
import os
from pandas.errors import EmptyDataError
from etl_process.extract.extract_github_client import busca_usuario
from etl_process.transform.transform_data import ajustar_dados
from etl_process.load.perfil_load import salva_log, salva_unique

HIST_CSV = "datausuarios.csv"
LOG_CSV = "data/log.csv"
USERS_CSV = "data/users.csv"

# Titulo da página.
st.title("GitHub Profile Viewer")
st.write("Exibição dos dados públicos de um perfil do GitHub")

# Criando o input aonde será feito a extração do usuário
username = st.text_input("Digite o nome do usuário GitHub: ")

if st.button("Buscar"):
    raw = busca_usuario(username)
    if raw is None:
        st.error("Falha na extração. Verifique o usuário e tente novamente.")
    else:
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

if st.button("Ver usuários únicos"):
    if not os.path.exists(USERS_CSV) or os.path.getsize(USERS_CSV) == 0:
        st.warning("Ainda não há usuários únicos salvos. Clique em Buscar para gerar o arquivo.")
    else:
        try:
            df_users = pd.read_csv(
                USERS_CSV, parse_dates=["created_at", "updated_at"]
            )
            st.dataframe(df_users)
        except EmptyDataError:
            st.warning("O arquivo de usuários está vazio.")