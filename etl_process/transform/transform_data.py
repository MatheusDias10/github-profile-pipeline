"""
Este módulo contém funções para limpar e transformar os dados
de um DataFrame.
"""

import pandas as pd


def ajustar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e normaliza um DataFrame bruto de dados de perfil GitHub.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame bruto com todas as colunas retornadas pela API.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo apenas as colunas:
        - login (str)
        - public_repos (int)
        - followers (int)
        - following (int)
        - created_at (datetime64[ns])
        - updated_at (datetime64[ns])
        - account_age (int)
    Raises
    ------
    TypeError
        Se `df` não for um pandas.DataFrame.
    ValueError
        Se `df` estiver vazio ou se falhar alguma conversão (datas ou numéricos).
    KeyError
        Se faltar alguma das colunas esperadas em `df`.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Esperando pd.DataFrame, mas recebeu {type(df)!r}")
    if df.empty:
        raise ValueError("DataFrame de entrada está vazio")

    cols = ["login",
            "public_repos",
            "followers",
            "following",
            "created_at",
            "updated_at"
        ]
    # Verificando se há faltantes
    faltantes = set(cols) - set(df.columns)
    if faltantes:
        raise KeyError(f"Colunas faltantes em DataFrame: {faltantes}")

    df_limpo = df[cols].copy()

    # Conversão de colunas de data (tratando tz-aware)
    try:
        df_limpo[["created_at", "updated_at"]] = (
            df_limpo[["created_at", "updated_at"]]
            .apply(lambda col: pd.to_datetime(col, utc=True).dt.tz_localize(None))
        )
    except Exception as e:
        raise ValueError(f"Falha ao converter datas: {e}") from e

    # Garantiundo que as colunas numéricas estarão em int
    df_limpo[["public_repos", "followers", "following"]] = (
        df_limpo[["public_repos", "followers", "following"]]
        .apply(pd.to_numeric)
    )

    # Criando uma coluna que mede o tempo da conta em dias
    df_limpo["account_age"] = (pd.Timestamp.now() - df_limpo["created_at"]).dt.days

    # Reset do Índice
    df_limpo = df_limpo.reset_index(drop=True)

    return df_limpo
