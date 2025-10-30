# gestao_financeira_rural.py
import json
from datetime import datetime
from collections import defaultdict

ARQUIVO_JSON = "financeiro.json"
ARQUIVO_TXT  = "relatorio.txt"

# despesas com categorias fixas
CATEGORIAS_DESPESA = ("Insumos", "Energia", "Mão de Obra", "Manutenção")

lancamentos = []  # tabela em memória (lista de dicionários)

# ------------------ Arquivos ------------------
def carregar_dados():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_dados():
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(lancamentos, f, indent=2, ensure_ascii=False)

# ------------------ Validações ------------------
def validar_data(data_str: str) -> bool:
    """Valida formato e data real YYYY-MM-DD."""
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validar_categoria(tipo: str, categoria: str) -> bool:
    """Receita: categoria livre; Despesa: uma das fixas."""
    if tipo == "RECEITA":
        return bool(categoria.strip())
    return categoria in CATEGORIAS_DESPESA

def validar_valor_positivo(valor_str: str):
    """Valor > 0 (para receitas)."""
    try:
        v = float(valor_str.replace(",", "."))
        if v <= 0:
            print("Valor deve ser maior que zero.")
            return None
        return round(v, 2)
    except ValueError:
        print("Valor inválido. Use números (ex.: 1500.75).")
        return None

def validar_valor_nao_negativo(valor_str: str):
    """Valor >= 0 (para gastos em lote; 0 significa não registrar aquela categoria)."""
    if valor_str.strip() == "":
        return 0.0
    try:
        v = float(valor_str.replace(",", "."))
        if v < 0:
            print("Valor não pode ser negativo.")
            return None
        return round(v, 2)
    except ValueError:
        print("Valor inválido. Use números (ex.: 1500.75).")
        return None

# ------------------ Regras e cálculos ------------------
def registrar_lancamento(tipo, descricao, valor, categoria, data):
    """Adiciona um lançamento na tabela e salva no JSON."""
    lancamentos.append({
        "id": len(lancamentos) + 1,
        "tipo": tipo,
        "data": data,
        "categoria": categoria.strip(),
        "descricao": descricao.strip(),
        "valor": round(valor, 2),
    })
    salvar_dados()

def registrar_gastos_lote(data, insumos, energia, mao_obra, manutencao, descricao="Gastos do dia"):
    """Cria vários lançamentos de DESPESA de uma vez (apenas valores > 0)."""
    mapa = {
        "Insumos": insumos,
        "Energia": energia,
        "Mão de Obra": mao_obra,
        "Manutenção": manutencao,
    }
    criados = 0
    for cat, val in mapa.items():
        if val > 0:
            registrar_lancamento("DESPESA", f"{descricao} - {cat}", val, cat, data)
            criados += 1
    return criados

def calcular_resumo():
    receitas = sum(l["valor"] for l in lancamentos if l["tipo"] == "RECEITA")
    despesas = sum(l["valor"] for l in lancamentos if l["tipo"] == "DESPESA")
    return receitas, despesas, receitas - despesas

# ------------------ Relatório em tabela ------------------
def _formata_tabela(registros, colunas):
    """Gera tabela de texto com largura dinâmica."""
    larg = {c: max(len(c), max((len(f"{r.get(c, '')}") for r in registros), default=0)) for c in colunas}
    header = " | ".join(c.upper().ljust(larg[c]) for c in colunas)
    sep    = "-+-".join("-" * larg[c] for c in colunas)

    linhas = [header, sep]
    for r in registros:
        celulas = []
        for c in colunas:
            val = r.get(c, "")
            if c == "valor":
                s = f"R${val:.2f}"
                celulas.append(s.rjust(larg[c]))
            else:
                celulas.append(f"{val}".ljust(larg[c]))
        linhas.append(" | ".join(celulas))
    return "\n".join(linhas)

def gerar_relatorio_txt():
    """Gera relatório TXT: tabela completa + totais + gastos por categoria."""
    with open(ARQUIVO_TXT, "w", encoding="utf-8") as f:
        if not lancamentos:
            f.write("Nenhum lançamento registrado.\n")
            print(f"📄 Relatório salvo em '{ARQUIVO_TXT}'.")
            return

        colunas = ["id", "tipo", "data", "categoria", "descricao", "valor"]
        receitas, despesas, lucro = calcular_resumo()

        # agrupamento por mês
        from collections import defaultdict
        por_mes = defaultdict(list)
        for l in lancamentos:
            por_mes[l["data"][:7]].append(l)

        # gastos por categoria de despesa
        gastos_por_categoria = {cat: sum(l["valor"] for l in lancamentos if l["tipo"] == "DESPESA" and l["categoria"] == cat)
                                for cat in CATEGORIAS_DESPESA}

        f.write("===== RELATÓRIO FINANCEIRO RURAL =====\n")
        f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

        f.write("== Lançamentos ==\n")
        f.write(_formata_tabela(lancamentos, colunas))
        f.write("\n\n")

        f.write("== Saldo por mês ==\n")
        if por_mes:
            linhas_mes = []
            for mes in sorted(por_mes.keys()):
                r = sum(x["valor"] for x in por_mes[mes] if x["tipo"] == "RECEITA")
                d = sum(x["valor"] for x in por_mes[mes] if x["tipo"] == "DESPESA")
                linhas_mes.append({"mes": mes, "receitas": f"R${r:.2f}", "despesas": f"R${d:.2f}", "saldo": f"R${(r-d):.2f}"})
            f.write(_formata_tabela(linhas_mes, ["mes", "receitas", "despesas", "saldo"]))
        else:
            f.write("(sem dados por mês)\n")

        f.write("\n\n== Resumo Geral ==\n")
        f.write(f"Total de Receitas: R${receitas:.2f}\n")
        f.write(f"Total de Despesas: R${despesas:.2f}\n")
        f.write(f"Lucro Final:       R${lucro:.2f}\n\n")

        f.write("== Gastos por Categoria ==\n")
        for cat, val in gastos_por_categoria.items():
            f.write(f"{cat:<15}: R${val:.2f}\n")

    print(f"📄 Relatório salvo em '{ARQUIVO_TXT}'.")

# ------------------ Menu (match/case) ------------------
def menu():
    global lancamentos
    lancamentos = carregar_dados()

    while True:
        print("\n==== Gestão Financeira Rural ====")
        print("1. Registrar Receita (categoria livre)")
        print("2. Registrar Gastos")
        print("3. Listar Lançamentos")
        print("4. Mostrar Resumo")
        print("5. Gerar Relatório")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                descricao = input("Descrição: ").strip()
                if not descricao:
                    print("A descrição não pode estar vazia.")
                    continue

                valor = validar_valor_positivo(input("Valor (R$): ").strip())
                if valor is None:
                    continue

                categoria = input("Categoria da receita (livre): ").strip()
                if not validar_categoria("RECEITA", categoria):
                    print("Categoria inválida para receita.")
                    continue

                data = input("Data (YYYY-MM-DD): ").strip()
                if not validar_data(data):
                    print("Data inválida. Use o formato YYYY-MM-DD e uma data existente.")
                    continue

                registrar_lancamento("RECEITA", descricao, valor, categoria, data)
                print("✅ Receita registrada.")

            case "2":
                print("Informe a DATA única para este conjunto de gastos.")
                data = input("Data (YYYY-MM-DD): ").strip()
                if not validar_data(data):
                    print("Data inválida.")
                    continue

                print("Digite os valores (use 0 ou deixe em branco para pular):")
                v_insumos    = validar_valor_nao_negativo(input("Insumos (R$): ").strip())
                if v_insumos is None:   continue
                v_energia    = validar_valor_nao_negativo(input("Energia (R$): ").strip())
                if v_energia is None:   continue
                v_mao_obra   = validar_valor_nao_negativo(input("Mão de Obra (R$): ").strip())
                if v_mao_obra is None:  continue
                v_manut      = validar_valor_nao_negativo(input("Manutenção (R$): ").strip())
                if v_manut is None:     continue

                if (v_insumos + v_energia + v_mao_obra + v_manut) == 0:
                    print("Nenhum valor informado (> 0). Nada para registrar.")
                    continue

                desc_padrao = input("Descrição: ").strip() or "Gastos do dia"
                criados = registrar_gastos_lote(data, v_insumos, v_energia, v_mao_obra, v_manut, desc_padrao)
                print(f"✅ {criados} gasto(s) registrado(s).")

            case "3":
                if not lancamentos:
                    print("(nenhum lançamento)")
                else:
                    print(_formata_tabela(lancamentos, ["id", "tipo", "data", "categoria", "descricao", "valor"]))

            case "4":
                r, d, l = calcular_resumo()
                print(f"\nReceitas: R${r:.2f} | Despesas: R${d:.2f} | Lucro: R${l:.2f}")

            case "5":
                gerar_relatorio_txt()

            case "0":
                print("Encerrando... até logo!")
                break

            case _:
                print("Opção inválida! Tente novamente.")

# ------------------ Execução ------------------
if __name__ == "__main__":
    menu()
