"""
Criando uma função que irá exportar e salvar o DataFrame em um arquivo CSV.
"""

from .db_config import engine
import pandas as pd


def carrega_historico(caminho: str) -> pd.DataFrame:
    """
    Lê o CSV de histórico de perfis e devolve um DataFrame.
    """
    return pd.read_csv(caminho, parse_dates=["created_at", "updated_at"])


def salva_log(df: pd.DataFrame) -> None:
    """
    Insere cada linha do DataFrame em log_perfis no SQL Server.
    """
    df.to_sql(
        name="log_perfis",
        con=engine,
        if_exists="append",
        index=False
    )


def salva_unique(df: pd.DataFrame) -> None:
    """
    Atualiza a tabela usuarios_unicos sem duplicatas.
    """
    try:
        df0 = pd.read_sql("SELECT * FROM usuarios_unicos", engine, parse_dates=["created_at","updated_at"])
    except Exception:
        df0 = pd.DataFrame()

    df_full = pd.concat([df0, df], ignore_index=True)
    df_full = df_full.drop_duplicates(subset=["login"], keep="last")

    df_full.to_sql(
        name="usuarios_unicos",
        con=engine,
        if_exists="replace",
        index=False
    )
