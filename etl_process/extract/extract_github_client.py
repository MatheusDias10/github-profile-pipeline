"""
Este módulo contém funções para buscar perfis de usuários no GitHub
e transformá-los em pandas DataFrames.
"""

import os
from json import JSONDecodeError

from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

headers = {
    "User-Agent": "github-profile-pipeline",
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}",
}

if not token:
    # token é None ou ""
    raise RuntimeError("GITHUB_TOKEN não definido. Verifique o arquivo .env")

session = requests.Session()
session.headers.update(headers)


def busca_usuario(username: str) -> pd.DataFrame | None:
    """
    Busca dados de perfil público de um usuário no GitHub.

    Parameters
    ----------
    username : str
        Nome do usuário (login) no GitHub a ser buscado.

    Returns
    -------
    pd.DataFrame | None
        DataFrame com as colunas de interesse ou None em caso de erro.
    """
    url = f"https://api.github.com/users/{username}"

    try:
        response = session.get(url, timeout=(3, 5))
        response.raise_for_status()
        data = response.json()
    except JSONDecodeError as e:
        print(f"Não foi possivel decodificar o JSON: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro: {e}")
    else:
        df = pd.DataFrame.from_dict([data])
        return df
    return None


if __name__ == "__main__":
    user = input("Qual o nome do perfil GitHub: ")
    busca_usuario(user)
