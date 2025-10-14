# Aplicação FarmTech Solutions: Milho e Café
# Suporte a cálculo de área, manejo de insumos e menu interativo

culturas = ['milho', 'cafe']
dados_milho = []  # Cada item: {'area': float, 'insumos': float}
dados_cafe = []   # Cada item: {'area': float, 'insumos': float}

def calcular_area_milho(comprimento, largura):
	# Área retangular para milho
	return comprimento * largura

def calcular_area_cafe(lado):
	# Área quadrada para café
	return lado * lado

def calcular_insumos_milho(area, quantidade_por_m2):
	return area * quantidade_por_m2

def calcular_insumos_cafe(area, quantidade_por_m2):
	return area * quantidade_por_m2

def menu():
	while True:
		print("\n--- Menu FarmTech Solutions ---")
		print("1. Entrada de dados")
		print("2. Exportar dados")
		print("3. Atualizar dados")
		print("4. Deletar dados")
		print("5. Sair")
		opcao = input("Escolha uma opção: ")
		if opcao == '1':
			entrada_dados()
		elif opcao == '2':
			saida_dados()
		elif opcao == '3':
			atualizar_dados()
		elif opcao == '4':
			deletar_dados()
		elif opcao == '5':
			print("Saindo...")
			break
		else:
			print("Opção inválida!")

def entrada_dados():
	print("\nEntrada de dados:")
	cultura = input("Digite a cultura (milho/cafe): ").lower()
	if cultura == 'milho':
		comprimento = float(input("Comprimento da área (m): "))
		largura = float(input("Largura da área (m): "))
		area = calcular_area_milho(comprimento, largura)
		produto = input("Produto a aplicar: ")
		quantidade_por_metro = float(input("Quantidade por metro (L/m): "))
		num_ruas = int(input("Quantas ruas a lavoura tem? "))
		total_litros = quantidade_por_metro * comprimento * num_ruas
		dados_milho.append({'area': area, 'produto': produto, 'quantidade_por_metro': quantidade_por_metro, 'num_ruas': num_ruas, 'total_litros': total_litros})
		print(f"Dados de milho adicionados: área={area:.2f} m², produto={produto}, total={total_litros:.2f} L para {num_ruas} ruas")
	elif cultura == 'cafe':
		lado = float(input("Lado da área (m): "))
		area = calcular_area_cafe(lado)
		produto = input("Produto a aplicar: ")
		quantidade_por_metro = float(input("Quantidade por metro (L/m): "))
		num_ruas = int(input("Quantas ruas a lavoura tem? "))
		total_litros = quantidade_por_metro * lado * num_ruas
		dados_cafe.append({'area': area, 'produto': produto, 'quantidade_por_metro': quantidade_por_metro, 'num_ruas': num_ruas, 'total_litros': total_litros})
		print(f"Dados de café adicionados: área={area:.2f} m², produto={produto}, total={total_litros:.2f} L para {num_ruas} ruas")
	else:
		print("Cultura inválida!")

def saida_dados():
	# Exportar dados para CSV
	exportar_csv()
def exportar_csv():
	import csv
	with open('dados_agricultura.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(['cultura', 'area', 'produto', 'quantidade_por_metro', 'num_ruas', 'total_litros'])
		for dado in dados_milho:
			writer.writerow([
				'milho',
				f"{dado['area']:.2f}",
				dado['produto'],
				dado['quantidade_por_metro'],
				dado['num_ruas'],
				f"{dado['total_litros']:.2f}"
			])
		for dado in dados_cafe:
			writer.writerow([
				'cafe',
				f"{dado['area']:.2f}",
				dado['produto'],
				dado['quantidade_por_metro'],
				dado['num_ruas'],
				f"{dado['total_litros']:.2f}"
			])
	print("\nExportar dados:")
	print("Milho:")
	for i, dado in enumerate(dados_milho):
		print(f"[{i}] Área: {dado['area']:.2f} m², Produto: {dado['produto']}, Quantidade por metro: {dado['quantidade_por_metro']} L/m, Ruas: {dado['num_ruas']}, Total: {dado['total_litros']:.2f} L")
	print("Café:")
	for i, dado in enumerate(dados_cafe):
		print(f"[{i}] Área: {dado['area']:.2f} m², Produto: {dado['produto']}, Quantidade por metro: {dado['quantidade_por_metro']} L/m, Ruas: {dado['num_ruas']}, Total: {dado['total_litros']:.2f} L")
	print("\nArquivo 'dados_agricultura.csv' exportado com sucesso!")

def atualizar_dados():
	print("\nAtualizar dados:")
	cultura = input("Digite a cultura (milho/cafe): ").lower()
	if cultura == 'milho' and dados_milho:
		print("Dados atuais de milho:")
		for i, dado in enumerate(dados_milho):
			print(f"[{i}] Área: {dado['area']:.2f} m², Produto: {dado['produto']}, Quantidade por metro: {dado['quantidade_por_metro']} L/m, Ruas: {dado['num_ruas']}, Total: {dado['total_litros']:.2f} L")
		idx = int(input("Índice do dado a atualizar: "))
		if 0 <= idx < len(dados_milho):
			comprimento = float(input("Novo comprimento (m): "))
			largura = float(input("Nova largura (m): "))
			area = calcular_area_milho(comprimento, largura)
			produto = input("Novo produto a aplicar: ")
			quantidade_por_metro = float(input("Nova quantidade por metro (L/m): "))
			num_ruas = int(input("Novo número de ruas: "))
			total_litros = quantidade_por_metro * comprimento * num_ruas
			dados_milho[idx] = {'area': area, 'produto': produto, 'quantidade_por_metro': quantidade_por_metro, 'num_ruas': num_ruas, 'total_litros': total_litros}
			print("Dado de milho atualizado!")
		else:
			print("Índice inválido!")
	elif cultura == 'cafe' and dados_cafe:
		print("Dados atuais de café:")
		for i, dado in enumerate(dados_cafe):
			print(f"[{i}] Área: {dado['area']:.2f} m², Produto: {dado['produto']}, Quantidade por metro: {dado['quantidade_por_metro']} L/m, Ruas: {dado['num_ruas']}, Total: {dado['total_litros']:.2f} L")
		idx = int(input("Índice do dado a atualizar: "))
		if 0 <= idx < len(dados_cafe):
			lado = float(input("Novo lado (m): "))
			area = calcular_area_cafe(lado)
			produto = input("Novo produto a aplicar: ")
			quantidade_por_metro = float(input("Nova quantidade por metro (L/m): "))
			num_ruas = int(input("Novo número de ruas: "))
			total_litros = quantidade_por_metro * lado * num_ruas
			dados_cafe[idx] = {'area': area, 'produto': produto, 'quantidade_por_metro': quantidade_por_metro, 'num_ruas': num_ruas, 'total_litros': total_litros}
			print("Dado de café atualizado!")
		else:
			print("Índice inválido!")
	else:
		print("Cultura inválida ou sem dados!")

def deletar_dados():
	print("\nDeletar dados:")
	cultura = input("Digite a cultura (milho/cafe): ").lower()
	if cultura == 'milho' and dados_milho:
		print("Dados atuais de milho:")
		for i, dado in enumerate(dados_milho):
			print(f"[{i}] Área: {dado['area']:.2f} m², Produto: {dado['produto']}, Quantidade por metro: {dado['quantidade_por_metro']} L/m, Ruas: {dado['num_ruas']}, Total: {dado['total_litros']:.2f} L")
		idx = int(input("Índice do dado a deletar: "))
		if 0 <= idx < len(dados_milho):
			dados_milho.pop(idx)
			print("Dado de milho deletado!")
		else:
			print("Índice inválido!")
	elif cultura == 'cafe' and dados_cafe:
		print("Dados atuais de café:")
		for i, dado in enumerate(dados_cafe):
			print(f"[{i}] Área: {dado['area']:.2f} m², Produto: {dado['produto']}, Quantidade por metro: {dado['quantidade_por_metro']} L/m, Ruas: {dado['num_ruas']}, Total: {dado['total_litros']:.2f} L")
		idx = int(input("Índice do dado a deletar: "))
		if 0 <= idx < len(dados_cafe):
			dados_cafe.pop(idx)
			print("Dado de café deletado!")
		else:
			print("Índice inválido!")
	else:
		print("Cultura inválida ou sem dados!")

if __name__ == "__main__":
	menu()
