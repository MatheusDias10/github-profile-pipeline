from etl_process.load.perfil_load import salva_csv
import pandas as pd

# DataFrame inventado
df = pd.DataFrame([{"login":"octocat","public_repos":5,"followers":42,
                    "following":3,"created_at":"2020-01-01T00:00:00Z",
                    "updated_at":"2025-05-26T12:00:00Z"}])
# Tenta salvar em data/octocat.csv
salva_csv(df, "data/teste.csv")