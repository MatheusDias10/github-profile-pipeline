"""
Pipeline completa.
"""

from etl_process.extract.extract_github_client import busca_usuario
from etl_process.transform.transform_data import ajustar_dados
from etl_process.load.perfil_load import salva_csv

if __name__ == "__main__":
    # Peça o user
    username = input("Qual o nome do perfil GitHub: ")
    # Rodar ETL
    raw = busca_usuario(username)
    if raw is None:
        print("Falha na extração. Verifique o usuário e tente novamente.")
    clean = ajustar_dados(raw)
    # Defina o caminho de saída
    output_path = f"data{username}.csv"
    salva_csv(clean, output_path)
    print(f"Concluido. Dados salvos em {output_path}")
