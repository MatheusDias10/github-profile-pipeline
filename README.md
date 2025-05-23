# github-profile-pipeline

Pipeline Python que extrai dados de perfis do GitHub via API, limpa com pandas e exporta para CSV.

---

## Visão Geral

Este projeto fornece um pipeline ETL simples para:

1. **Extrair** dados de perfis GitHub usando a API oficial.
2. **Transformar** o JSON bruto em um DataFrame pandas, mantendo apenas os campos relevantes.
3. **Carregar** os resultados em arquivos CSV para análises ou integração com outros sistemas.

Ideal para quem deseja comparar características de usuários (número de repositórios, seguidores, data de criação, etc.) de forma automatizada.

---

## Recursos Principais

* Busca de perfis GitHub autenticada via token (Personal Access Token).
* Tratamento de erros de rede e parsing de JSON.
* Garantia de configuração de ambiente (.env) e feedback claro em caso de falta de credenciais.
* Modularização em fases Extract e Transform, com possibilidade de extensão para Load.
* Retorno de DataFrames pandas prontos para análise e exportação.

---

## Tecnologias Utilizadas

* **Python 3.10+**
* **pandas 2.2.3**
* **requests 2.32.3**
* **python-dotenv 1.1.0**

---

## Estrutura do Projeto

```text
github-profile-pipeline/
│
├── .venv/                            # Ambiente virtual
├── etl_process/                      # Pasta principal do pipeline ETL
│   ├── 1_extract_data/               # Módulo de extração
│   │   └── extract_github_profile.py # Função de extração de perfis
│   ├── 2_transform/                  # Módulo de transformação
│   │   └── transform_data.py         # Limpeza e normalização de dados
│   └── 3_load/                       # Módulo de carregamento
│       └── perfil_load.py            # Funções de persistência (CSV, banco, etc.)
├── .env                              # Variáveis de ambiente
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/MatheusDias10/github-profile-pipeline.git
   cd github-profile-pipeline
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração

1. Crie um arquivo `.env` na raiz do projeto:

   ```dotenv
   GITHUB_TOKEN=seu_personal_access_token_aqui
   ```
2. Certifique-se de que `.env` está listado no `.gitignore` para não vazar credenciais.
