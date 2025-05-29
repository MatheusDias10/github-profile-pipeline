"""
Criando uma função que irá exportar e salvar o DataFrame em um arquivo CSV.
"""

import os
import pandas as pd


def salva_csv(df: pd.DataFrame, caminho: str, append: bool = False) -> None:
    """
    Persiste o DataFrame em um arquivo CSV.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame já transformado e pronto para a exportação.
    caminho: str
        Caminho é aonde será salvo o .csv.
    append: bool
        Quando for True o CSV será aberto em modo append e só
        terá cabeçalho caso o arquivo não exista.

    Raises
    ------
    ValueError
        Se df não for um DataFrame ou estiver vazio.
    OSError
        Se falhar a escrita do arquivo.
    """
    if append:
        modo = "a"
        header = not os.path.exists(caminho)
    else:
        modo = "w"
        header = True

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Esperando DataFrame mas recebeu {type(df)!r}")
    if df.empty:
        raise ValueError("DataFrame de entrada está vazio, nada para salvar.")

    pasta = os.path.dirname(caminho)

    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)

    # Grava o CSV no caminho informado
    df.to_csv(caminho, mode=modo, header=header, index=False)

def carrega_historico(caminho: str) -> pd.DataFrame:
    """
    Lê o CSV de histórico de perfis e devolve um DataFrame.
    """
    return pd.read_csv(caminho, parse_dates=["created_at", "updated_at"])

def salva_log(df: pd.DataFrame, path: str) -> None:
    # decide se deve incluir cabeçalho
    header = not os.path.exists(path)
    df.to_csv(path, mode="a", header=header, index=False)

def salva_unique(df: pd.DataFrame, path: str) -> None:
    """
    Atualiza a lista unica de usuários (users.cvs), sem duplicatas.
    """

    # Vendo se a pasta existe no disco e caso True coloque-as em dtype
    if os.path.exists(path) and os.path.getsize(path) > 0:
        df0 = pd.read_csv(path, parse_dates=["created_at","updated_at"])
    else:
        df0 = pd.DataFrame()

    # Concatenar e tirar duplicatas.
    df_full = pd.concat([df0, df], ignore_index=True)
    df_full = df_full.drop_duplicates(subset=["login"], keep="last")

    # Aplica no csv.
    df_full.to_csv(path, index=False)

if __name__ == "__main__":
    salva_csv(pd.DataFrame(), "data.csv")
