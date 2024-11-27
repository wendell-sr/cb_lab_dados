import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__)
DATA_LAKE_PATH = "data_lake/raw"  # Caminho base do Data Lake

@app.route("/api/data-lake", methods=["GET"])
def query_data_lake():
    """
    Consulta o Data Lake na estrutura loja > data > endpoint.
    """
    store_id = request.args.get("storeId")
    date = request.args.get("date")
    endpoint = request.args.get("endpoint")

    # Validação dos parâmetros
    if not store_id or not date or not endpoint:
        return jsonify({"error": "Parâmetros 'storeId', 'date' e 'endpoint' são obrigatórios"}), 400

    # Monta o caminho correto com base na nova estrutura
    folder_path = os.path.join(DATA_LAKE_PATH, store_id, date)
    file_path = os.path.join(folder_path, f"{endpoint}.json")

    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        return jsonify({"error": f"Arquivo não encontrado: {file_path}"}), 404

    # Carrega os dados do arquivo JSON
    with open(file_path, "r") as file:
        data = json.load(file)

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
