import os
import json

DATA_LAKE_PATH = "data_lake/raw"

def save_api_response(folder_structure, filename, response):
    """
    Salva a resposta da API na estrutura loja > data > endpoint.
    
    :param folder_structure: Estrutura hierárquica (ex.: "store_001/2024-11-27").
    :param filename: Nome do arquivo JSON (ex.: "getGuestChecks.json").
    :param response: Resposta da API (em JSON).
    """
    # Cria a hierarquia de pastas com base na estrutura fornecida
    folder_path = os.path.join(DATA_LAKE_PATH, folder_structure)
    os.makedirs(folder_path, exist_ok=True)

    # Define o caminho completo do arquivo
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w") as file:
        json.dump(response, file, indent=4)
    print(f"Response saved to {file_path}")
