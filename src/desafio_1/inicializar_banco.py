import os
import json
import sqlite3
import pandas as pd

# Caminhos fixos para os dados e banco
DATA_PATH = "data/ERP.json"
DB_PATH = "data/restaurante.sqlite"


def limpar_dataframe(df):
    """
    Limpa o DataFrame para garantir compatibilidade com SQLite:
    - Substitui valores None ou NaN por valores padrão.
    - Converte listas ou dicionários para strings.
    """
    for coluna in df.columns:
        df[coluna] = df[coluna].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)
    return df.fillna("").convert_dtypes()


def criar_datasets_a_partir_do_json(arquivo_json):
    """
    Processa o JSON ERP.json e retorna os DataFrames:
    - contas
    - taxas
    - itens_detalhados
    - itens_menu
    """
    with open(arquivo_json, "r") as file:
        dados = json.load(file)

    # Extraindo contas
    dados_contas = dados.get("guestChecks", [])
    contas = pd.json_normalize(dados_contas)
    contas.rename(
        columns={
            "guestCheckId": "id_conta",
            "chkNum": "numero_conta",
            "opnBusDt": "data_abertura",
            "clsdBusDt": "data_fechamento",
            "subTtl": "subtotal",
            "chkTtl": "total_conta",
            "payTtl": "total_pago",
            "empNum": "id_funcionario",
        },
        inplace=True,
    )

    # Processando taxas
    taxas = []
    for conta in dados_contas:
        for taxa in conta.get("taxes", []):
            entrada_taxa = taxa.copy()
            entrada_taxa["id_conta"] = conta["guestCheckId"]
            taxas.append(entrada_taxa)
    df_taxas = pd.DataFrame(taxas)
    df_taxas.rename(
        columns={
            "taxNum": "id_taxa",
            "txblSlsTtl": "vendas_tributadas",
            "taxCollTtl": "valor_taxa",
            "taxRate": "aliquota",
        },
        inplace=True,
    )

    # Processando itens detalhados e itens do menu
    itens_detalhados = []
    itens_menu = []
    itens_menu_ids = set()  # Para evitar duplicados

    for conta in dados_contas:
        for item in conta.get("detailLines", []):
            # Processa itens detalhados
            item_menu = item.get("menuItem", {})
            entrada_item_detalhado = {
                "id_item_detalhado": item["guestCheckLineItemId"],
                "id_conta": conta["guestCheckId"],
                "id_item_menu": item_menu.get("miNum"),
                "quantidade": item.get("dspQty"),
                "preco_total": item.get("dspTtl"),
            }
            itens_detalhados.append(entrada_item_detalhado)

            # Processa itens do menu (elimina duplicados)
            id_menu = item_menu.get("miNum")
            if id_menu not in itens_menu_ids:
                itens_menu_ids.add(id_menu)
                entrada_item_menu = {
                    "id_item_menu": id_menu,
                    "modificavel": item_menu.get("modFlag"),
                    "taxas_incluidas": item_menu.get("inclTax"),
                    "taxas_ativas": item_menu.get("activeTaxes"),
                    "nivel_preco": item_menu.get("prcLvl"),
                }
                itens_menu.append(entrada_item_menu)

    df_itens_detalhados = pd.DataFrame(itens_detalhados)
    df_itens_menu = pd.DataFrame(itens_menu)

    # Limpa os DataFrames
    contas = limpar_dataframe(contas)
    df_taxas = limpar_dataframe(df_taxas)
    df_itens_detalhados = limpar_dataframe(df_itens_detalhados)
    df_itens_menu = limpar_dataframe(df_itens_menu)

    return contas, df_taxas, df_itens_detalhados, df_itens_menu


def criar_tabelas(conexao):
    """
    Cria as tabelas no banco de dados SQLite com nomes e estrutura traduzidos.
    """
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id_conta INTEGER PRIMARY KEY,
            numero_conta INTEGER,
            data_abertura TEXT,
            data_fechamento TEXT,
            subtotal REAL,
            total_conta REAL,
            total_pago REAL,
            id_funcionario INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS taxas (
            id_taxa INTEGER,
            id_conta INTEGER,
            vendas_tributadas REAL,
            valor_taxa REAL,
            aliquota REAL,
            tipo_taxa INTEGER,
            PRIMARY KEY (id_taxa, id_conta),
            FOREIGN KEY (id_conta) REFERENCES contas (id_conta)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_detalhados (
            id_item_detalhado INTEGER PRIMARY KEY,
            id_conta INTEGER,
            id_item_menu INTEGER,
            quantidade INTEGER,
            preco_total REAL,
            FOREIGN KEY (id_conta) REFERENCES contas (id_conta),
            FOREIGN KEY (id_item_menu) REFERENCES itens_menu (id_item_menu)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_menu (
            id_item_menu INTEGER PRIMARY KEY,
            modificavel BOOLEAN,
            taxas_incluidas REAL,
            taxas_ativas TEXT,
            nivel_preco INTEGER
        );
    """)

    print("Tabelas criadas com sucesso!")
    cursor.close()


def inicializar_banco(arquivo_json, caminho_banco):
    """
    Inicializa o banco de dados SQLite e carrega os dados do arquivo JSON.
    """
    if not os.path.exists(arquivo_json):
        print(f"Erro: Arquivo JSON não encontrado em {arquivo_json}")
        return

    # Conecta ao banco de dados SQLite
    conexao = sqlite3.connect(caminho_banco)
    print(f"Conectado ao banco de dados: {caminho_banco}")

    # Criar tabelas no banco
    criar_tabelas(conexao)

    # Processar e carregar os dados
    print(f"Processando arquivo JSON: {arquivo_json}")
    contas, taxas, itens_detalhados, itens_menu = criar_datasets_a_partir_do_json(arquivo_json)

    contas.to_sql("contas", conexao, if_exists="replace", index=False)
    taxas.to_sql("taxas", conexao, if_exists="replace", index=False)
    itens_detalhados.to_sql("itens_detalhados", conexao, if_exists="replace", index=False)
    itens_menu.to_sql("itens_menu", conexao, if_exists="replace", index=False)

    conexao.close()
    print("Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    inicializar_banco(DATA_PATH, DB_PATH)
