import os
import json
import requests

DATA_LAKE_PATH = "data_lake/raw"  # Caminho base do Data Lake


def salvar_arquivo_loja(loja, data, endpoint, conteudo):
    """
    Salva os dados da API na estrutura de diretórios do Data Lake.
    """
    caminho_pasta = os.path.join(DATA_LAKE_PATH, loja, data)
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_arquivo = os.path.join(caminho_pasta, f"{endpoint}.json")
    with open(caminho_arquivo, "w") as arquivo:
        json.dump(conteudo, arquivo, indent=4)
    print(f"Arquivo salvo em: {caminho_arquivo}")


def consumir_api(loja, data, endpoint):
    """
    Faz uma requisição à API e salva os dados no Data Lake.
    """
    url = f"http://127.0.0.1:5000/api/{endpoint}?storeId={loja}&date={data}"
    try:
        print(f"Consumindo API: {url}")  # Log para depuração
        resposta = requests.get(url, timeout=10)  # Timeout de 10 segundos
        resposta.raise_for_status()
        salvar_arquivo_loja(loja, data, endpoint, resposta.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao consumir {endpoint} para loja {loja} na data {data}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erro de requisição ao consumir {endpoint} para loja {loja} na data {data}: {req_err}")
    except Exception as e:
        print(f"Erro inesperado ao consumir {endpoint} para loja {loja} na data {data}: {e}")


def criar_data_lake(lojas, datas, endpoints):
    """
    Percorre as lojas, datas e endpoints para consumir dados e armazenar no Data Lake.
    """
    for loja in lojas:
        for data in datas:
            for endpoint in endpoints:
                consumir_api(loja, data, endpoint)


if __name__ == "__main__":
    # Configurações para lojas, datas e endpoints
    lojas = ["001", "002"]  # IDs das lojas
    datas = ["2024-11-25", "2024-11-26", "2024-11-27"]  # Datas para as quais queremos dados
    endpoints = [
        "getGuestChecks",
        "getTransactions",
        "getFiscalInvoice",
        "getChargeBack",
        "getCashManagementDetails"
    ]

    # Executa a criação do Data Lake
    criar_data_lake(lojas, datas, endpoints)
