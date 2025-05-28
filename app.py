import streamlit as st
from etl_process.extract.extract_github_client import busca_usuario
from etl_process.transform.transform_data import ajustar_dados
from etl_process.load.perfil_load import salva_csv, carrega_historico
import os

HIST_CSV = "datausuarios.csv"


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
        salva_csv(clean, HIST_CSV, append=True)
        st.info(f"Perfil salvo em histórico: {HIST_CSV}")

if st.button("Ver histórico"):
    df_hist = carrega_historico(HIST_CSV)
    st.dataframe(df_hist)
