# Gestão Financeira Rural — CLI (Python)

Um aplicativo de terminal simples para **registrar receitas e despesas rurais**, salvar os dados em **JSON** e gerar um **relatório em tabela (TXT)** com totais por mês e por categoria de gasto.

> Projeto focado em estruturas e algoritmos **sem classes**, usando **funções** com **passagem de parâmetros**, e **estruturas de dados nativas** (lista, tupla, dicionário, tabela de memória).

---

## ✨ Funcionalidades

- **Menu interativo** com `match/case` (Python 3.10+).
- **Registro de receitas** (categoria livre).
- **Registro em lote de despesas** nas categorias fixas: `Insumos`, `Energia`, `Mão de Obra`, `Manutenção`.
- **Validações**:
  - Data no formato `YYYY-MM-DD` (e data real).
  - Categoria: livre para **RECEITA**; **fixa** para **DESPESA**.
  - Valores: receitas **> 0**; despesas em lote **≥ 0** (0 = ignora).
- **Tabela em memória** (lista de dicionários) + **persistência** em `financeiro.json`.
- **Relatório TXT** (`relatorio.txt`) com:
  - Tabela completa dos lançamentos
  - Resumo por mês (receitas, despesas e saldo)
  - Resumo geral (totais e lucro final)
  - **Gastos por categoria** (Insumos/Energia/Mão de Obra/Manutenção)

---

## 📁 Estrutura do Projeto

```
.
├─ gestao_financeira_rural.py   # código principal (CLI)
├─ financeiro.json               # base de dados (criado automaticamente)
└─ relatorio.txt                 # relatório em tabela (gerado sob demanda)
```

---

## 🧰 Requisitos

- **Python 3.10+** (por causa do `match/case`).
- **Sem dependências externas** (apenas biblioteca padrão: `json`, `datetime`, `collections`).

### Instalação opcional (Windows/Linux/macOS)

```bash
# (Opcional) criar e ativar um ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Não há pacotes a instalar — uso direto
```

---

## ▶️ Como Executar

Na pasta do projeto:

```bash
python gestao_financeira_rural.py
```

Você verá o menu:

```
==== Gestão Financeira Rural ====
1. Registrar Receita (categoria livre)
2. Registrar Gastos
3. Listar Lançamentos
4. Mostrar Resumo
5. Gerar Relatório
0. Sair
```

---

## 🧪 Exemplos de Uso (entrada pelo teclado)

### 1) Registrar **Receita**
- **Descrição**: Venda de milho
- **Valor (R$)**: `12500,75`  _(vírgula é aceita; ponto também)_
- **Categoria**: `Grãos`
- **Data**: `2025-10-10`  _(formato obrigatório `YYYY-MM-DD`)_

Resultado: um lançamento `RECEITA` é salvo (id incremental).

### 2) Registrar **Gastos em lote** (apenas valores > 0 geram lançamentos)

> Dica: use `0` ou deixe **em branco** para pular aquela categoria.

- **Data**: `2025-10-10`  
- **Insumos (R$)**: `4545`  
- **Energia (R$)**: `0`  
- **Mão de Obra (R$)**: `500`  
- **Manutenção (R$)**: _(em branco)_  
- **Descrição**: `Gastos da colheita` _(padrão: "Gastos do dia")_

Resultado: são criados até **4 lançamentos** do tipo `DESPESA` (somente para valores > 0).

### 3) Listar Lançamentos

Mostra uma **tabela de texto** com colunas: `id | tipo | data | categoria | descricao | valor`.

### 4) Mostrar Resumo

Exibe: `Receitas | Despesas | Lucro` (valores acumulados de todo o período).

### 5) Gerar Relatório

Cria/atualiza o arquivo **`relatorio.txt`** com:
- **Lançamentos** (tabela completa);
- **Saldo por mês** (YYYY-MM com receitas, despesas, saldo);
- **Resumo Geral** (totais e lucro final);
- **Gastos por Categoria** (apenas DESPESA e nas 4 categorias fixas).

---

## 🧱 Estruturas de Dados Utilizadas

- **Tupla**: `CATEGORIAS_DESPESA = ("Insumos", "Energia", "Mão de Obra", "Manutenção")`
- **Lista**: `lancamentos = []` (tabela em memória)
- **Dicionário**: cada lançamento possui as chaves:
  - `id: int`
  - `tipo: "RECEITA" | "DESPESA"`
  - `data: "YYYY-MM-DD"`
  - `categoria: str`
  - `descricao: str`
  - `valor: float`
- **defaultdict(list)**: agrupamento de lançamentos por mês no relatório.

---

## 💾 Persistência (JSON)

O arquivo **`financeiro.json`** é criado automaticamente. Exemplo de conteúdo:

```json
[
  {
    "id": 1,
    "tipo": "RECEITA",
    "data": "2025-10-10",
    "categoria": "Grãos",
    "descricao": "Venda de milho",
    "valor": 12500.75
  },
  {
    "id": 2,
    "tipo": "DESPESA",
    "data": "2025-10-10",
    "categoria": "Insumos",
    "descricao": "Gastos da colheita - Insumos",
    "valor": 4545.0
  },
  {
    "id": 3,
    "tipo": "DESPESA",
    "data": "2025-10-10",
    "categoria": "Mão de Obra",
    "descricao": "Gastos da colheita - Mão de Obra",
    "valor": 500.0
  }
]
```

---

## 🧾 Exemplo (trecho) do `relatorio.txt`

```
===== RELATÓRIO FINANCEIRO RURAL =====
Gerado em: 15/10/2025 21:00:00

== Lançamentos ==
ID | TIPO    | DATA       | CATEGORIA   | DESCRICAO                    | VALOR
---+---------+------------+-------------+------------------------------+-----------
1  | RECEITA | 2025-10-10 | Grãos       | Venda de milho               |    R$12500.75
2  | DESPESA | 2025-10-10 | Insumos     | Gastos da colheita - Insumos |     R$4545.00
3  | DESPESA | 2025-10-10 | Mão de Obra | Gastos da colheita - Mão...  |      R$500.00

== Saldo por mês ==
MES      | RECEITAS    | DESPESAS    | SALDO
---------+-------------+-------------+-------------
2025-10  | R$12500.75  | R$5045.00   | R$7455.75

== Resumo Geral ==
Total de Receitas: R$12500.75
Total de Despesas: R$5045.00
Lucro Final:       R$7455.75

== Gastos por Categoria ==
Insumos        : R$4545.00
Energia        : R$0.00
Mão de Obra    : R$500.00
Manutenção     : R$0.00
```

> A largura das colunas é **dinâmica**, calculada a partir do conteúdo real, para manter a tabela legível.

---

## ✅ Regras de Validação (resumo)

- **Data**: `validar_data()` usa `datetime.strptime` e **recusa** datas inexistentes.
- **Categoria**: `validar_categoria()` permite **qualquer** categoria para `RECEITA`, mas **restringe** a `DESPESA` às 4 categorias fixas.
- **Valores**:
  - `validar_valor_positivo()` — receitas precisam ser **> 0**.
  - `validar_valor_nao_negativo()` — despesas em lote aceitam **≥ 0** (0 = não registra).
  - Ambos aceitam vírgula **ou** ponto decimal.

---

## 🔍 Dicas e Observações

- O **ID** é gerado automaticamente (1, 2, 3, …) com base no total em memória.
- Para **quebrar linha** longa na descrição da tabela, a lógica mantém o texto e ajusta a largura — evite descrições exageradamente grandes.
- **Moedas** são formatadas como `R$#.##` somente na exibição; internamente, armazenadas como `float` (duas casas na gravação).

---

## 🧯 Solução de Problemas (FAQ)

**1) O programa não abre ou dá erro de versão.**  
Use `python --version` e garanta `3.10+`.

**2) Digitei data `2025-02-30` e deu “Data inválida”.**  
A validação garante **datas reais** — ajuste o dia/mês.

**3) Usei vírgula nos valores.**  
Aceito! O código converte `,` → `.` internamente.

**4) O relatório está vazio.**  
Cadastre ao menos um lançamento (receita ou despesa) e gere novamente pelo menu **[5]**.

---

## 📜 Licença

Código educacional de uso livre. Adapte conforme sua necessidade acadêmica ou pessoal.
