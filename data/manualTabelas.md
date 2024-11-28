# **Manual das Tabelas do Banco de Dados**

## **Tabela: contas**
- **Descrição**: Representa as contas de clientes no restaurante, contendo informações como datas, valores e funcionário associado.
- **Fonte no JSON**: Atributo `guestChecks`.

### **Estrutura**
| Nome da Coluna       | Tipo     | Descrição                                        | Mapeamento no JSON          |
|----------------------|----------|------------------------------------------------|-----------------------------|
| `id_conta`           | INTEGER  | Identificador único da conta (PK)              | `guestCheckId`              |
| `numero_conta`       | INTEGER  | Número da conta                                | `chkNum`                    |
| `data_abertura`      | TEXT     | Data de abertura da conta                      | `opnBusDt`                  |
| `data_fechamento`    | TEXT     | Data de fechamento da conta                    | `clsdBusDt`                 |
| `subtotal`           | REAL     | Subtotal da conta                              | `subTtl`                    |
| `total_conta`        | REAL     | Total da conta                                 | `chkTtl`                    |
| `total_pago`         | REAL     | Valor total pago                               | `payTtl`                    |
| `id_funcionario`     | INTEGER  | Identificador do funcionário responsável       | `empNum`                    |

### **Relações**
- Relaciona-se com a tabela **`taxas`** (1:N) via `id_conta`.
- Relaciona-se com a tabela **`itens_detalhados`** (1:N) via `id_conta`.

---

## **Tabela: taxas**
- **Descrição**: Contém informações sobre as taxas aplicadas a cada conta, como impostos ou outras cobranças.
- **Fonte no JSON**: Subatributo `taxes` dentro de `guestChecks`.

### **Estrutura**
| Nome da Coluna         | Tipo     | Descrição                                      | Mapeamento no JSON          |
|------------------------|----------|----------------------------------------------|-----------------------------|
| `id_taxa`              | INTEGER  | Identificador único da taxa (PK composta)    | `taxNum`                    |
| `id_conta`             | INTEGER  | Identificador da conta (FK para `contas`)    | Relacionado com `guestCheckId` |
| `vendas_tributadas`    | REAL     | Total das vendas tributadas                  | `txblSlsTtl`                |
| `valor_taxa`           | REAL     | Valor da taxa cobrada                        | `taxCollTtl`                |
| `aliquota`             | REAL     | Alíquota da taxa aplicada                    | `taxRate`                   |
| `tipo_taxa`            | INTEGER  | Tipo de taxa                                 | `type`                      |

### **Relações**
- Relaciona-se com a tabela **`contas`** (N:1) via `id_conta`.

---

## **Tabela: itens_detalhados**
- **Descrição**: Contém os itens consumidos em cada conta, como pratos e bebidas.
- **Fonte no JSON**: Atributo `detailLines` dentro de `guestChecks`.

### **Estrutura**
| Nome da Coluna         | Tipo     | Descrição                                      | Mapeamento no JSON          |
|------------------------|----------|----------------------------------------------|-----------------------------|
| `id_item_detalhado`    | INTEGER  | Identificador único do item (PK)             | `guestCheckLineItemId`      |
| `id_conta`             | INTEGER  | Identificador da conta (FK para `contas`)    | Relacionado com `guestCheckId` |
| `id_item_menu`         | INTEGER  | Identificador do item no menu (FK para `itens_menu`) | `menuItem.miNum`      |
| `quantidade`           | INTEGER  | Quantidade consumida                         | `dspQty`                    |
| `preco_total`          | REAL     | Preço total do item                          | `dspTtl`                    |

### **Relações**
- Relaciona-se com a tabela **`contas`** (N:1) via `id_conta`.
- Relaciona-se com a tabela **`itens_menu`** (N:1) via `id_item_menu`.

---

## **Tabela: itens_menu**
- **Descrição**: Representa os itens disponíveis no cardápio, com informações como preço, modificações e taxas aplicáveis.
- **Fonte no JSON**: Subatributo `menuItem` dentro de `detailLines`.

### **Estrutura**
| Nome da Coluna         | Tipo     | Descrição                                      | Mapeamento no JSON          |
|------------------------|----------|----------------------------------------------|-----------------------------|
| `id_item_menu`         | INTEGER  | Identificador único do item do menu (PK)     | `miNum`                     |
| `modificavel`          | BOOLEAN  | Indica se o item pode ser modificado         | `modFlag`                   |
| `taxas_incluidas`      | REAL     | Valor das taxas incluídas no item            | `inclTax`                   |
| `taxas_ativas`         | TEXT     | Identificadores das taxas aplicáveis         | `activeTaxes`               |
| `nivel_preco`          | INTEGER  | Nível de preço do item                       | `prcLvl`                    |

### **Relações**
- Relaciona-se com a tabela **`itens_detalhados`** (1:N) via `id_item_menu`.

---

## **Relações Entre as Tabelas**

```
contas
  ├── taxas (1:N)
  └── itens_detalhados (1:N)
         └── itens_menu (N:1)
```

### **Explicação**
1. **`contas`** é a tabela principal, representando cada conta aberta no restaurante.
2. **`taxas`** contém as informações das taxas aplicadas às contas.
3. **`itens_detalhados`** lista os itens consumidos em cada conta, como pratos ou bebidas.
4. **`itens_menu`** armazena os detalhes fixos dos itens disponíveis no menu.

---

