# Documentação do Projeto CB_LAB_DADOS

## Introdução

Este projeto foi desenvolvido para resolver o desafio do CBLAB relacionado à engenharia de dados. Ele consiste em duas partes principais:

1. **Desafio 1**: Estruturar um banco de dados a partir de um arquivo JSON.
2. **Desafio 2**: Estruturar um Data Lake, simular APIs, e implementar uma API para consultas e manipulação.

## Tecnologias Utilizadas

- **Python**: Manipulação de dados, criação de APIs e scripts.
- **SQLite**: Banco de dados relacional para persistência dos dados.
- **Flask**: Framework para criação de APIs.
- **Docker**: Ambiente isolado para execução dos scripts.
- **Markdown**: Documentação.

## Estrutura do Projeto

```
CB_LAB_DADOS/
|— data/                       # Dados de entrada e banco gerado
|   |— ERP.json                # Arquivo JSON principal para inicializar o banco
|   |— restaurante.sqlite      # Banco de dados SQLite gerado
|   |— manualTabelas.md       # Manual de descrição das tabelas
|— data_lake/                 # Estrutura do Data Lake
|   |— raw/                   # Dados brutos organizados
|       |— 001/               # Loja 001
|           |— 2024-11-25/    # Dados do dia
|               |— getGuestChecks.json
|               |— getTransactions.json
|               |— getFiscalInvoice.json
|               |— getChargeBack.json
|               |— getCashManagementDetails.json
|— src/                        # Scripts do projeto
|   |— desafio_1/             # Scripts relacionados ao Desafio 1
|       |— inicializar_banco.py   # Inicializa o banco a partir do ERP.json
|   |— desafio_2/             # Scripts relacionados ao Desafio 2
|       |— criar_data_lake_respostas_api.py  # Cria o Data Lake consumindo a API
|       |— manipular_data_lake.py            # Manipulações no Data Lake
|       |— simular_api.py                   # Simula a API com os 5 endpoints
|— docker-compose.yml          # Configuração do Docker Compose
|— Dockerfile                  # Configuração do container Docker
|— README.md                   # Documentação do projeto
```

---

## Desafio 1: Banco de Dados

### **Objetivo**

Inicializar um banco de dados SQLite a partir do arquivo `ERP.json`, criando tabelas organizadas e relacionando os dados conforme descrito no manual.

### **Tabela Criadas**

1. **Contas**:
   - Armazena as informações das contas abertas por clientes.
   - **Colunas**: id_conta, num_conta, data_abertura, subtotal, total.

2. **Itens Detalhados**:
   - Detalha os itens do menu que fazem parte de uma conta.
   - **Colunas**: id_item, id_conta (FK), nome_item, preco.

3. **Taxas**:
   - Registra as taxas aplicadas sobre os itens ou contas.
   - **Colunas**: id_taxa, descricao_taxa, valor_taxa.

4. **Menu**:
   - Armazena informações gerais dos itens do menu.
   - **Colunas**: id_menu, nome_item, preco_base, ativo.

### **Execução**

1. Inicializar o banco de dados:
   ```bash
   python src/desafio_1/inicializar_banco.py
   ```

2. Resultado esperado:
   - Arquivo gerado: `data/restaurante.sqlite`

3. Consultar o banco:
   - Use ferramentas como **DB Browser for SQLite** para visualizar os dados.

---

## Desafio 2: Data Lake

### **Objetivo**

Criar e manipular uma estrutura de Data Lake para armazenar os dados de 5 endpoints simulados:

- **getGuestChecks**
- **getTransactions**
- **getFiscalInvoice**
- **getChargeBack**
- **getCashManagementDetails**

### **Fluxo de Execução**

#### 1. Simular API

- Inicialize a API simulada para fornecer dados dos endpoints:
  ```bash
  python src/desafio_2/simular_api.py
  ```

#### 2. Criar o Data Lake

- Consuma os endpoints e organize os dados na estrutura do Data Lake:
  ```bash
  python src/desafio_2/criar_data_lake_respostas_api.py
  ```

- Arquivos gerados em:
  ```
  data_lake/raw/{storeId}/{date}/{endpoint}.json
  ```

#### 3. Manipular Data Lake

- API para manipular e consultar os dados do Data Lake:
  ```bash
  python src/desafio_2/manipular_data_lake.py
  ```

- **Endpoints Disponíveis**:
  1. **Consultar dados**:
     ```bash
     curl "http://127.0.0.1:5000/api/data-lake?storeId=001&date=2024-11-25&endpoint=getGuestChecks"
     ```

  2. **Atualizar dados**:
     ```bash
     curl -X POST "http://127.0.0.1:5000/api/data-lake" \
          -H "Content-Type: application/json" \
          -d '{"storeId": "001", "date": "2024-11-25", "endpoint": "getGuestChecks", "data": [{"id": 3, "subtotal": 150.0, "total": 180.0}]}'
     ```

  3. **Excluir dados**:
     ```bash
     curl -X DELETE "http://127.0.0.1:5000/api/data-lake?storeId=001&date=2024-11-25&endpoint=getGuestChecks"
     ```

  4. **Buscar e filtrar dados**:
     ```bash
     curl "http://127.0.0.1:5000/api/search?storeId=001&date=2024-11-25&endpoint=getGuestChecks&key=id&value=1"
     ```

---

## Docker

### **Configuração**

- **Dockerfile**: Configuração do container para executar os scripts do projeto.
- **docker-compose.yml**: Configuração do ambiente com suporte a Flask e SQLite.

### **Comandos**

1. Construir a imagem:
   ```bash
   docker-compose build
   ```

2. Iniciar o container:
   ```bash
   docker-compose up
   ```

3. Acessar o container:
   ```bash
   docker exec -it cb_lab_dados-app sh
   ```

---

## Considerações Finais

Este projeto foi estruturado para atender às necessidades dos dois desafios, promovendo uma separação clara entre banco de dados e manipulação de Data Lake. Ele é flexível e pode ser facilmente adaptado para novos requisitos.

