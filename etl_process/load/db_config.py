"""
etl_process/load/db_config.py
"""

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Lê variáveis de ambiente, com defaults seguros
host = os.getenv("MSSQL_HOST", "localhost")
port = os.getenv("MSSQL_PORT", "1433")
database = os.getenv("MSSQL_DATABASE", "GitHubProfiles")

# Monta a URL de conexão para Windows Auth (trusted connection)
connection_str = (
    f"mssql+pyodbc://@{host}:{port}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

# Cria um engine global para a aplicação inteira
engine = create_engine(connection_str)
