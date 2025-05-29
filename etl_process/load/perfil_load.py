"""
Criando uma função que irá exportar e salvar o DataFrame em um arquivo CSV.
"""

import os
import pandas as pd


def carrega_historico(caminho: str) -> pd.DataFrame:
    """
    Lê o CSV de histórico de perfis e devolve um DataFrame.
    """
    return pd.read_csv(caminho, parse_dates=["created_at", "updated_at"])


def salva_log(df: pd.DataFrame, path: str) -> None:
    """
    Decide se deve incluir cabeçarios e coloca o df no modo append
    """
    header = not os.path.exists(path)
    df.to_csv(path, mode="a", header=header, index=False)


def salva_unique(df: pd.DataFrame, path: str) -> None:
    """
    Atualiza a lista unica de usuários (users.cvs), sem duplicatas.
    """

    # Vendo se a pasta existe no disco e caso True coloque-as em dtype
    if os.path.exists(path) and os.path.getsize(path) > 0:
        df0 = pd.read_csv(path, parse_dates=["created_at", "updated_at"])
    else:
        df0 = pd.DataFrame()

    # Concatenar e tirar duplicatas.
    df_full = pd.concat([df0, df], ignore_index=True)
    df_full = df_full.drop_duplicates(subset=["login"], keep="last")

    # Aplica no csv.
    df_full.to_csv(path, index=False)
