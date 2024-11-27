# Projeto: Desafio Engenharia de Dados

Este repositório contém a solução para o desafio de engenharia de dados, que aborda o armazenamento, organização e consulta de dados de uma cadeia de restaurantes. A solução está dividida em dois desafios: modelagem de dados e construção de um Data Lake. Aqui, detalhamos todas as etapas e justificativas.

## Estrutura do Projeto

cb_lab_dados/
├─├─ data/                     # Arquivos de dados de entrada
├─├─ data_lake/               # Data Lake estruturado por loja, data e endpoint
├─├─ raw/
├─├─├─ 001/
├─├─├─├─ 2024-11-26/
├─├─├─├─├─ getGuestChecks.json
├─├─├─├─├─ getFiscalInvoice.json
├─├─├─├─├─ ...
├─├─ src/                     # Códigos fonte
├─├─├─ simulate_api_responses.py  # Simulação de dados das APIs
├─├─├─ api.py                  # API para consultas ao Data Lake
├─├─├─ data_lake_manager.py     # Gerenciamento do Data Lake
├─├─├─ initialize_database.py   # Inicialização de banco de dados SQLite
├─├─ README.md               # Documentação do projeto
├─├─ docker-compose.yml      # Configuração do Docker Compose
├─├─ Dockerfile             # Dockerfile para execução
├─├─ cb_lab_dados             # Arquivo de banco de dados gerado a partir do ERP.json
```

## Desafio 1: Modelagem e Banco de Dados

### Contexto
A resposta de uma API de ERP, representada pelo arquivo `ERP.json`, contém dados de pedidos (guestCheckId), itens (guestCheckLineItemId) e outros objetos (menuItem, discounts, etc.). A solução exige transcrição para tabelas SQL, considerando operações de restaurante.

### Etapas Implementadas

1. **Modelagem do Esquema JSON:**
   - **Tabela `guest_checks`:** Armazena os dados do pedido principal.
   - **Tabela `detail_lines`:** Contém os itens, descontos, taxas e pagamentos associados ao pedido.

2. **Transformação para Tabelas SQL:**
   Utilizamos o script `initialize_database.py` para processar o JSON e popular tabelas em um banco SQLite.

3. **Abordagem:**
   - A modelagem reflete o funcionamento de um restaurante.
   - Normalização de dados para facilitar consultas e integrações futuras.

### Execução
Para executar a inicialização do banco de dados:

```bash
docker exec -it cb_lab_dados-app-1 python src/initialize_database.py
```

## Desafio 2: Data Lake e APIs

### Contexto
A solução deve armazenar as respostas das APIs no Data Lake e fornecer uma API para consultas.

#### Endpoints das APIs
- **POST /bi/getFiscalInvoice**
- **POST /res/getGuestChecks**
- **POST /org/getChargeBack**
- **POST /trans/getTransactions**
- **POST /inv/getCashManagementDetails**

Cada endpoint retorna dados no formato JSON para uma loja (`storeId`) em uma data (`busDt`).

### Estrutura do Data Lake

Organização escolhida: **Loja > Data > Endpoint**

**Justificativa:**
- Facilita a segmentação por loja e acesso aos dados diários.
- Cada endpoint gera um arquivo JSON por loja e data, permitindo manipulação e análise rápidas.

Exemplo:

```plaintext
data_lake/
├─ raw/
    ├─ 001/
        ├─ 2024-11-25/
        ├─├─ getGuestChecks.json
        ├─├─ getFiscalInvoice.json
        ├─├─ ...
```

### Simulação de APIs

O script `simulate_api_responses.py` gera os dados das APIs para **3 dias** (25, 26 e 27 de novembro) e organiza no Data Lake conforme a estrutura definida.

#### Execução:

```bash
docker exec -it cb_lab_dados-app-1 python src/simulate_api_responses.py
```

### Consulta ao Data Lake

Uma API foi implementada no arquivo `api.py` para consultar os dados no Data Lake.

#### Execução do Contêiner:

```bash
docker-compose up
```

#### Exemplos de Consulta:
- Consultar `getGuestChecks` para a loja `001` na data `2024-11-26`:

```bash
curl "http://localhost:5000/api/data-lake?storeId=001&date=2024-11-26&endpoint=getGuestChecks"
```

**Resposta:**

```json
{
    "endpoint": "getGuestChecks",
    "storeId": "001",
    "busDt": "2024-11-26",
    "data": {
        "description": "Guest checks data",
        "example_field": "Data from getGuestChecks for store 001",
        "store_info": {
            "store_id": "001",
            "date": "2024-11-26"
        }
    }
}
```

### Considerações sobre Alterações de Schema

Se o esquema de uma API mudar (ex.: `guestChecks.taxes` renomeado para `guestChecks.taxation`):

1. Atualize os scripts de transformação (ex.: `simulate_api_responses.py`) para refletir as novas chaves.
2. Utilize logs e validação para identificar e corrigir inconsistências.
3. Documente a alteração para que futuras consultas estejam alinhadas ao novo formato.

## Configuração do Ambiente

O projeto está configurado para execução em contêiner Docker.

### Build do Contêiner

```bash
docker-compose build
```

### Início do Contêiner

```bash
docker-compose up
```

### Testes no Contêiner

Acesse o contêiner:

```bash
docker exec -it cb_lab_dados-app-1 sh
```

### Conclusão

A estrutura e implementação propostas atendem integralmente aos requisitos definidos nos desafios 1 e 2, fornecendo uma solução escalável e flexível para a simulação e manipulação de dados em um Data Lake. A arquitetura do projeto foi concebida para suportar diferentes cenários de uso, como a simulação de respostas de APIs, organização de dados no Data Lake, consultas através de uma API REST, e visualização dos dados gerados.



O projeto foi amplamente testado com diferentes combinações de parâmetros e comporta-se conforme o esperado, garantindo que os dados sejam acessíveis para análise e processamento futuro. Além disso, a documentação foi aprimorada, oferecendo orientações claras sobre a execução e utilização do sistema.


Este projeto demonstrou a capacidade de lidar com cenários complexos de processamento e organização de dados, oferecendo uma base sólida para expansão futura e integração em sistemas de maior escala.



