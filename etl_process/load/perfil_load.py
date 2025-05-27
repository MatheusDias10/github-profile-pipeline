"""
Criando uma função que irá exportar e salvar o DataFrame em um arquivo CSV.
"""

import os
import pandas as pd


def salva_csv(df: pd.DataFrame, caminho: str) -> None:
    """
    Persiste o DataFrame em um arquivo CSV.
    
    Parameters
    ----------
    df: pd.DataFrame
        DataFrame já transformado e pronto para a exportação.
    caminho: str
        Caminho é aonde será salvo o .csv.
    
    Raises
    ------
    ValueError
        Se df não for um DataFrame ou estiver vazio.
    OSError
        Se falhar a escrita do arquivo.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Esperando DataFrame mas recebeu {type(df)!r}")
    if df.empty:
        raise ValueError("DataFrame de entrada está vazio, nada para salvar.")
    
    pasta = os.path.dirname(caminho)
    
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
    
    # Grava o CSV no caminho informado
    df.to_csv(caminho, index=False)
    
if __name__ == "__main__":
    salva_csv(pd.DataFrame(), "data.csv")