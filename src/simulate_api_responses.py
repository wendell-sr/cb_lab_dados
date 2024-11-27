from data_lake_manager import save_api_response
from datetime import datetime, timedelta

def simulate_api_responses():
    """
    Simula a geração e armazenamento de respostas de APIs para múltiplas datas.
    Estrutura: loja > data > endpoint.
    """
    endpoints = {
        "getFiscalInvoice": {"description": "Fiscal invoice data"},
        "getGuestChecks": {"description": "Guest checks data"},
        "getChargeBack": {"description": "Chargeback data"},
        "getTransactions": {"description": "Transactions data"},
        "getCashManagementDetails": {"description": "Cash management details"}
    }
    stores = ["001", "002"]  # IDs de lojas

    # Gerar os dados para os dias 25, 26 e 27
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 3)]

    for store_id in stores:
        for date in dates:
            for endpoint, meta in endpoints.items():
                response = {
                    "endpoint": endpoint,
                    "storeId": store_id,
                    "busDt": date,
                    "data": {
                        "description": meta["description"],
                        "example_field": f"Data from {endpoint} for store {store_id} on {date}",
                        "store_info": {"store_id": store_id, "date": date}
                    }
                }
                # Ajuste para refletir a nova estrutura do Data Lake
                folder_structure = f"{store_id}/{date}"
                save_api_response(folder_structure, f"{endpoint}.json", response)

if __name__ == "__main__":
    simulate_api_responses()
