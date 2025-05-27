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
│   ├── extract_data/               # Módulo de extração
│   │   └── extract_github_profile.py # Função de extração de perfis
│   ├── transform/                  # Módulo de transformação
│   │   └── transform_data.py         # Limpeza e normalização de dados
│   └── load/                       # Módulo de carregamento
│       └── perfil_load.py            # Funções de persistência (CSV, banco, etc.)
├── .env                              # Variáveis de ambiente
├── .gitattributes
├── .gitignore
├── LICENSE
├── pipeline.py                       # Aonde vai rodar o arquivo principal contendo todas as funções  
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

---

## Uso

### Extrair um único perfil

```bash
python extract.py
Qual o nome do perfil GitHub:
```

### Pipeline completo ETL

```bash
python pipeline.py --username octocat --output data/octocat.csv
```

Onde:

* `--username`: login do GitHub a ser buscado.
* `--output`: caminho do CSV de saída.

---

## Exemplo de Resultado

O arquivo CSV terá colunas como:

| login   | public_repos | followers | following | created_at          | updated_at          | account_age |
| ------- | ------------ | --------- | --------- | ------------------- | ------------------- | ----------- |
| octocat | 8            | 5256      | 9         | 2011-01-25T18:44:36Z | 2025-05-02T07:45:05Z | 5211      |


---

## Contribuindo

1. Fork este repositório.
2. Crie uma branch de feature (`git checkout -b feature/minha-feature`).
3. Implemente as mudanças e escreva testes, se aplicável.
4. Faça commit e push da sua branch.
5. Abra um Pull Request descrevendo suas alterações.

---

## Licença

Este projeto está licenciado sob a **BSD 3-Clause License**. Consulte o arquivo `LICENSE` para mais detalhes.

---

## Autor

Feito por: MatheusDias10 – [LinkedIn](https://www.linkedin.com/in/matheus-dias-71982b333/)
