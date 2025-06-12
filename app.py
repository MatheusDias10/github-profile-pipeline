"""
Fazendo a interface web rodar com todo o prrocesso ETL embutido.
"""

import pandas as pd
import streamlit as st

from etl_process.extract.extract_github_client import busca_usuario
from etl_process.transform.transform_data import ajustar_dados
from etl_process.load.functions import salva_log, salva_unique
from etl_process.load.db_config import engine
from sqlalchemy import text


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
            salva_log(clean)
            salva_unique(clean)

            # Deixando apenas os "avisos" sem a tabela
            st.success("Dados carregados com sucesso.")

    # Botão para ver o histórico
    if st.button("Ver histórico"):
        st.session_state["exibir_historico"] = True

    # Botão para ver os usuários únicos
    if st.button("Ver usuários únicos"):
        st.session_state["exibir_usuarios_unicos"] = True

    # Criando um botão de limpar os dados das tabelas.
    if st.button("Limpar dados da tabela"):
        # tenta ler quantas linhas existem
        try:
            count_users = pd.read_sql("SELECT COUNT(*) FROM usuarios_unicos", engine).iloc[0,0]
            count_log = pd.read_sql("SELECT COUNT(*) FROM log_perfis",     engine).iloc[0,0]
        except Exception:
            st.warning("Não foi possível acessar as tabelas no banco.")
            st.stop()

        # se estiver tudo vazio, aborta
        if count_users == 0 and count_log == 0:
            st.warning("Não há dados para limpar.")
            st.stop()

        # se chegou aqui, é porque EXISTEM linhas a serem removidas
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM usuarios_unicos;"))
            conn.execute(text("DELETE FROM log_perfis;"))

        # limpa o estado e avisa sucesso
        st.session_state.clear()
        st.success("O histórico foi limpo.")


# EXIBIÇÃO NA ÁREA PRINCIPAL

# Se o usuário clicou em "Buscar" mostramos a tabela na área principal
if st.session_state.get("exibir_perfil", False):
    df = st.session_state["perfil_df"]
    st.dataframe(df)    # Tabela do perfil GitHub fica na área principal

# Se clicou em "Ver histórico", mostramos o log completo na área principal
if st.session_state.get("exibir_historico", False):
    try:
        df_log = pd.read_sql(
            "SELECT * FROM log_perfis",  # nome da tabela no banco
            engine,
            parse_dates=["created_at", "updated_at"]
        )
        if df_log.empty:
            st.warning("Ainda não há histórico salvo. Clique em Buscar antes.")
        else:
            st.dataframe(df_log)
    except Exception:
        st.warning("Ainda não há histórico salvo. Clique em Buscar antes.")

# Se clicou em "Ver usuários únicos", mostramso a lista única na área principal
if st.session_state.get("exibir_usuarios_unicos", False):
    try:
        df_users = pd.read_sql(
            "SELECT * FROM usuarios_unicos",
            engine,
            parse_dates=["created_at", "updated_at"]
        )
        if df_users.empty:
            st.warning("Ainda não há usuários únicos salvos. Clique em Buscar antes.")
        else:
            st.dataframe(df_users)
    except Exception:
        st.warning("Ainda não há usuários únicos salvos. Clique em Buscar antes.")
