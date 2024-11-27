import os
import json
import sqlite3
import pandas as pd

# Caminhos fixos para os dados e banco
DATA_PATH = "data/ERP.json"
DB_PATH = "data/cb_lab_dados.sqlite"


def clean_dataframe(df):
    """
    Limpa o DataFrame para garantir compatibilidade com SQLite:
    - Substitui valores None ou NaN por valores padrão.
    - Converte listas ou dicionários para strings.
    """
    for column in df.columns:
        df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)
    return df.fillna("").convert_dtypes()


def create_datasets_from_json(json_file):
    """
    Processa o JSON ERP.json e retorna três DataFrames:
    - guest_checks: Dados normalizados do JSON principal.
    - taxes: Dados de impostos aninhados.
    - detail_lines: Dados detalhados de itens aninhados.
    """
    with open(json_file, "r") as file:
        data = json.load(file)

    # Extraindo guestChecks
    guest_checks_data = data.get("guestChecks", [])
    guest_checks = pd.json_normalize(guest_checks_data)

    # Processando impostos (taxes)
    taxes = []
    for check in guest_checks_data:
        for tax in check.get("taxes", []):
            tax_entry = tax.copy()
            tax_entry["guestCheckId"] = check["guestCheckId"]
            taxes.append(tax_entry)
    taxes_df = pd.DataFrame(taxes)

    # Processando linhas detalhadas (detailLines)
    detail_lines = []
    for check in guest_checks_data:
        for line in check.get("detailLines", []):
            line_entry = line.copy()
            line_entry["guestCheckId"] = check["guestCheckId"]
            detail_lines.append(line_entry)
    detail_lines_df = pd.DataFrame(detail_lines)

    # Limpa os DataFrames
    guest_checks = clean_dataframe(guest_checks)
    taxes_df = clean_dataframe(taxes_df)
    detail_lines_df = clean_dataframe(detail_lines_df)

    return guest_checks, taxes_df, detail_lines_df


def initialize_database(data_path, db_path):
    """
    Inicializa o banco de dados SQLite e carrega os dados do arquivo JSON.
    """
    # Verifica se o arquivo JSON existe
    if not os.path.exists(data_path):
        print(f"Erro: Arquivo JSON não encontrado em {data_path}")
        return

    # Conecta ao banco de dados SQLite (cria se não existir)
    conn = sqlite3.connect(db_path)
    print(f"Conectado ao banco de dados: {db_path}")

    # Processa os dados do JSON
    print(f"Processando arquivo JSON: {data_path}")
    try:
        guest_checks, taxes, detail_lines = create_datasets_from_json(data_path)

        # Carrega os DataFrames no banco de dados
        guest_checks.to_sql("guest_checks", conn, if_exists="replace", index=False)
        taxes.to_sql("taxes", conn, if_exists="replace", index=False)
        detail_lines.to_sql("detail_lines", conn, if_exists="replace", index=False)

        print("Banco de dados inicializado com sucesso!")
    except ValueError as e:
        print(f"Erro ao processar o arquivo JSON: {e}")
    except sqlite3.InterfaceError as e:
        print(f"Erro ao inserir dados no SQLite: {e}")

    conn.close()


if __name__ == "__main__":
    initialize_database(DATA_PATH, DB_PATH)
