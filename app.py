"""
Fazendo a interface web rodar com todo o prrocesso ETL embutido.
"""

import os
import pandas as pd
import streamlit as st

from etl_process.extract.extract_github_client import busca_usuario
from etl_process.transform.transform_data import ajustar_dados
from etl_process.load.perfil_load import salva_log, salva_unique


LOG_CSV = "data/log.csv"
USERS_CSV = "data/users.csv"


# COnfiguração da pagina para sidebar
st.set_page_config(
    page_title="GitHub Profile Viewer",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Titulo da página
st.title("GitHub Profile Viewer")
st.write("Exibição dos dados públicos de um perfil do GitHub")

# COntroles na Sidebar
with st.sidebar:
    username = st.text_input("Digite o nome do usuário GitHub: ")

    # Criando os botões
    if st.button("Buscar"):
        raw = busca_usuario(username)
        if raw is None:
            st.error("Falha na extração. Verifique o usuário e tente novamente.")
        else:
            # Limpando os dados do df "raw" que recebeu os dados do usuario
            clean = ajustar_dados(raw)

            st.session_state["exibir_perfil"] = True
            st.session_state["perfil_df"] = clean

            # Atualiza log completo e a lista única
            salva_log(clean, LOG_CSV)
            salva_unique(clean, USERS_CSV)

            st.info(f"Perfil adicionado ao log: {LOG_CSV}")
            st.info(f"Lista única atualizada: {USERS_CSV}")

            # Deixando apenas os "avisos" sem a tabela
            st.success("Dados carregados com sucesso.")
            st.info(f"Perfil adicionado ao log: {LOG_CSV}")
            st.info(f"Lista única atualizada: {USERS_CSV}")

    # Botão para ver o histórico
    if st.button("Ver histórico"):
        st.session_state["exibir_historico"] = True

    # Botão para ver os usuários únicos
    if st.button("Ver usuários únicos"):
        st.session_state["exibir_usuarios_unicos"]

    # Criando um botão de limpar os dados das tabelas.
    if st.button("Limpar dados da tabela"):
        # Lógico da limpeza do CSV
        st.success("O histórico foi limpo.")

# EXIBIÇÃO NA ÁREA PRINCIPAL

# Se o usuário clicou em "Buscar" mostramos a tabela na área principal
if st.session_state.get("exibir_perfil", False):
    df = st.session_state["perfil_df"]
    st.dataframe(df)    # Tabela do perfil GitHub fica na área principal

# Se clicou em "Ver histórico", mostramos o log completo na área principal
if st.session_state.get("exibir_historico", False):
    # Antes, conferindo se o arquivo existe ou se está vazio
    if not os.path.exists(LOG_CSV) or os.path.getsize(LOG_CSV) == 0:
        st.warning("Ainda não há histórico salvo. Clique em Buscar antes.")
    else:
        df_log = pd.read_csv(LOG_CSV, parse_dates=["created_at", "updated_at"])
        st.dataframe(df_log)

# Se clicou em "Ver usuários únicos", mostramso a lista única na área principal
if st.session_state.get("exibir_usuarios_unicos", False):
    if not os.path.exists(USERS_CSV) or os.path.getsize(USERS_CSV) == 0:
        st.warning("Ainda não há usuários únicos salvos. Clique em Buscar antes.")
    else:
        df_users = pd.read_csv(USERS_CSV, parse_dates=["created_at", "updated_at"])
        st.dataframe(df_users)
    

# PROBLEMA: NÃO ESTÁ LIMPANDO OS DADOS DA TABELA AO CLICAR NO "LIMPAR HISTÓRICO".
