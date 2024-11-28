# **Respostas ao Desafio de Engenharia de Dados**

## **Desafio 1**

### **1. Esquema JSON correspondente ao exemplo fornecido**

O arquivo `ERP.json` contém a estrutura de dados utilizada pelo sistema ERP. Abaixo está um exemplo do esquema JSON processado:

```
jsonCopiar código{
  "guestCheckId": 1122334455,
  "chkNum": 1234,
  "opnBusDt": "2024-01-01",
  "opnUTC": "2024-01-01T09:09:09",
  "detailLines": [
    {
      "guestCheckLineItemId": 1,
      "menuItem": {
        "miNum": 6042,
        "modFlag": false,
        "inclTax": 20.809091,
        "activeTaxes": [28],
        "prcLvl": 3
      },
      "discount": {
        "amount": 10.0,
        "reason": "Cupom de desconto"
      },
      "serviceCharge": {
        "amount": 5.0,
        "description": "Serviço adicional"
      },
      "tenderMedia": {
        "amount": 100.0,
        "type": "Cartão de Crédito"
      },
      "errorCode": "ERR123"
    }
  ]
}
```

------

### **2. Tabelas SQL derivadas do JSON**

A partir do JSON, foram geradas as seguintes tabelas no banco de dados SQLite:

#### **Tabela `contas`**

Registra informações gerais de cada conta (pedido):

```
sqlCopiar códigoCREATE TABLE contas (
    id_conta INTEGER PRIMARY KEY,
    numero_conta INTEGER,
    data_abertura TEXT,
    horario_abertura_utc TEXT
);
```

Exemplo de dado inserido:

| id_conta | numero_conta | data_abertura | horario_abertura_utc |
| -------- | ------------ | ------------- | -------------------- |
| 1        | 1234         | 2024-01-01    | 2024-01-01T09:09:09  |

------

#### **Tabela `itens_detalhados`**

Registra os itens associados a uma conta:

```
sqlCopiar códigoCREATE TABLE itens_detalhados (
    id_item INTEGER PRIMARY KEY,
    id_conta INTEGER,
    id_menu_item INTEGER,
    valor_total REAL,
    desconto_motivo TEXT,
    taxa_servico_descricao TEXT,
    meio_pagamento_tipo TEXT,
    codigo_erro TEXT,
    FOREIGN KEY (id_conta) REFERENCES contas(id_conta)
);
```

Exemplo de dado inserido:

| id_item | id_conta | id_menu_item | valor_total | desconto_motivo   | taxa_servico_descricao | meio_pagamento_tipo | codigo_erro |
| ------- | -------- | ------------ | ----------- | ----------------- | ---------------------- | ------------------- | ----------- |
| 1       | 1        | 6042         | 100.00      | Cupom de desconto | Serviço adicional      | Cartão de Crédito   | ERR123      |

------

#### **Tabela `menu_items`**

Armazena os itens de menu associados aos pedidos:

```
sqlCopiar códigoCREATE TABLE menu_items (
    id_menu_item INTEGER PRIMARY KEY,
    flag_modificador BOOLEAN,
    inclui_taxa REAL,
    niveis_ativos TEXT,
    nivel_preco INTEGER
);
```

Exemplo de dado inserido:

| id_menu_item | flag_modificador | inclui_taxa | niveis_ativos | nivel_preco |
| ------------ | ---------------- | ----------- | ------------- | ----------- |
| 6042         | false            | 20.809091   | 28            | 3           |

------

### **3. Abordagem Escolhida**

- **Escolha do SQLite**: Um banco de dados leve e portátil, ideal para o volume de dados de um restaurante e fácil integração com sistemas locais.
- **Normalização**: Divisão dos dados em tabelas relacionadas para reduzir redundância e facilitar a manipulação.
- **Escalabilidade**: A estrutura pode ser facilmente adaptada para novos campos ou requisitos.

------

## **Desafio 2**

### **1. Por que armazenar as respostas das APIs?**

- **Disponibilidade**: Reduz a dependência de APIs externas, garantindo acesso local aos dados mesmo em situações de falha.
- **Histórico de Dados**: Permite manter registros organizados por loja e data, possibilitando análises de tendências.
- **Rapidez**: Consultas locais são mais rápidas que chamadas constantes às APIs.
- **Conformidade**: Garante que os dados analisados sejam consistentes e estejam centralizados.

------

### **2. Estrutura de Armazenamento no Data Lake**

A seguinte estrutura foi definida no projeto para armazenar os dados:

```
yamlCopiar códigodata_lake/
└── raw/
    ├── 001/
    │   ├── 2024-11-25/
    │   │   ├── getGuestChecks.json
    │   │   ├── getTransactions.json
    │   │   ├── getFiscalInvoice.json
    │   │   ├── getChargeBack.json
    │   │   └── getCashManagementDetails.json
    │   ├── 2024-11-26/
    │   └── 2024-11-27/
    └── 002/
        ├── 2024-11-25/
        ├── 2024-11-26/
        └── 2024-11-27/
```

------

### **3. Alteração no Endpoint `getGuestChecks`**

Se o campo `guestChecks.taxes` fosse renomeado para `guestChecks.taxation`, os seguintes ajustes seriam necessários:

- **Scripts**: Ajustar o consumo no script `criar_data_lake_respostas_api.py`:

  ```
  python
  taxas = item.get("taxation") or item.get("taxes")
  ```

- **Banco de Dados**: Atualizar a tabela `taxas`:

  ```
  sql
  ALTER TABLE taxas RENAME COLUMN taxes TO taxation;
  ```

- **Data Lake**: Reprocessar arquivos antigos para refletir o novo nome.

------

## **Como rodar o projeto**

1. **Subir o ambiente com Docker:**

   ```
   bash
   docker-compose up
   ```

2. **Simular as APIs:**

   ```
   bash
   python src/desafio_2/simular_api.py
   ```

3. **Criar o Data Lake:**

   ```
   bash
   python src/desafio_2/criar_data_lake_respostas_api.py
   ```

4. **Consultar o Data Lake:**

   ```
   bash
   python src/desafio_2/manipular_data_lake.py
   ```

------

## **Conclusão**

O projeto aborda a solução de maneira escalável, modular e com foco em boas práticas. A estrutura relacional facilita análises de dados no contexto de restaurantes, enquanto o Data Lake permite a integração de dados para inteligência de negócios.