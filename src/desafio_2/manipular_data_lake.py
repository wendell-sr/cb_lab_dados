import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__)
DATA_LAKE_PATH = "data_lake/raw"  # Caminho base do Data Lake

@app.route("/api/data-lake", methods=["GET"])
def query_data_lake():
    """
    Consulta dados no Data Lake na estrutura loja > data > endpoint.
    """
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    endpoint = request.args.get("endpoint")

    # Validação dos parâmetros
    if not store_id or not date or not endpoint:
        return jsonify({"error": "Parâmetros 'storeId', 'date' e 'endpoint' são obrigatórios"}), 400

    # Monta o caminho correto com base na estrutura
    folder_path = os.path.join(DATA_LAKE_PATH, store_id, date)
    file_path = os.path.join(folder_path, f"{endpoint}.json")

    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        return jsonify({"error": f"Arquivo não encontrado: {file_path}"}), 404

    # Carrega os dados do arquivo JSON
    with open(file_path, "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/api/data-lake", methods=["POST"])
def update_data_lake():
    """
    Atualiza ou cria dados no Data Lake.
    """
    store_id = request.json.get("storeId")
    date = request.json.get("date")
    endpoint = request.json.get("endpoint")
    content = request.json.get("data")

    # Validação dos parâmetros
    if not store_id or not date or not endpoint or content is None:
        return jsonify({"error": "Parâmetros 'storeId', 'date', 'endpoint' e 'data' são obrigatórios"}), 400

    # Monta o caminho correto
    folder_path = os.path.join(DATA_LAKE_PATH, store_id, date)
    file_path = os.path.join(folder_path, f"{endpoint}.json")

    # Cria a estrutura de pastas, se necessário
    os.makedirs(folder_path, exist_ok=True)

    # Salva os dados no arquivo JSON
    with open(file_path, "w") as file:
        json.dump(content, file, indent=4)

    return jsonify({"message": f"Dados salvos em {file_path}"})

@app.route("/api/data-lake", methods=["DELETE"])
def delete_data_lake():
    """
    Exclui dados no Data Lake.
    """
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    endpoint = request.args.get("endpoint")

    # Validação dos parâmetros
    if not store_id or not date or not endpoint:
        return jsonify({"error": "Parâmetros 'storeId', 'date' e 'endpoint' são obrigatórios"}), 400

    # Monta o caminho correto
    folder_path = os.path.join(DATA_LAKE_PATH, store_id, date)
    file_path = os.path.join(folder_path, f"{endpoint}.json")

    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        return jsonify({"error": f"Arquivo não encontrado: {file_path}"}), 404

    # Remove o arquivo
    os.remove(file_path)

    return jsonify({"message": f"Arquivo {file_path} excluído com sucesso"})


@app.route("/api/search", methods=["GET"])
def search_data_lake():
    """
    Busca e filtra dados em um arquivo específico do Data Lake.
    """
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    endpoint = request.args.get("endpoint")
    search_key = request.args.get("key")
    search_value = request.args.get("value")

    # Validação dos parâmetros
    if not store_id or not date or not endpoint or not search_key or not search_value:
        return jsonify({"error": "Parâmetros 'storeId', 'date', 'endpoint', 'key' e 'value' são obrigatórios"}), 400

    # Monta o caminho correto
    folder_path = os.path.join(DATA_LAKE_PATH, store_id, date)
    file_path = os.path.join(folder_path, f"{endpoint}.json")

    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        return jsonify({"error": f"Arquivo não encontrado: {file_path}"}), 404

    # Carrega os dados do arquivo JSON
    with open(file_path, "r") as file:
        data = json.load(file)

    # Filtra os dados
    filtered_data = [item for item in data if str(item.get(search_key)) == search_value]

    return jsonify(filtered_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
