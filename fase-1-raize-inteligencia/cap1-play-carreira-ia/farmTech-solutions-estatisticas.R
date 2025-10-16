# Script R para calcular média e desvio padrão amostral dos dados de insumos
# Supondo que os dados estejam em vetores para milho e café

# Exemplo de dados (substitua pelos seus dados reais)
milho_total_litros <- c(120, 150, 130, 160)
cafe_total_litros <- c(80, 90, 85, 95)

# Função para calcular estatísticas básicas
dados_estatisticos <- function(vetor) {
  media <- mean(vetor)
  desvio <- sd(vetor)
  cat("Média:", media, "\n")
  cat("Desvio padrão amostral:", desvio, "\n")
}

# Calcular e exibir estatísticas
dados <- read.csv('dados_agricultura.csv', stringsAsFactors = FALSE)

# Separar os dados por cultura
milho <- subset(dados, cultura == 'milho')
cafe <- subset(dados, cultura == 'cafe')



# Bloco Milho
cat('====================\n')
cat('DADOS DE MILHO\n')
cat('====================\n')
for (i in 1:nrow(milho)) {
  cat(sprintf('Linha %d: Área=%s, Produto=%s, Quantidade por metro=%s, Ruas=%s, Total litros=%s\n',
              i,
              milho$area[i],
              milho$produto[i],
              milho$quantidade_por_metro[i],
              milho$num_ruas[i],
              milho$total_litros[i]))
}
cat('\nResumo estatístico para Milho:\n')
cat('Média:', mean(as.numeric(milho$total_litros)), '\n')
cat('Desvio padrão amostral:', sd(as.numeric(milho$total_litros)), '\n')

# Bloco Café
cat('\n====================\n')
cat('DADOS DE CAFÉ\n')
cat('====================\n')
for (i in 1:nrow(cafe)) {
  cat(sprintf('Linha %d: Área=%s, Produto=%s, Quantidade por metro=%s, Ruas=%s, Total litros=%s\n',
              i,
              cafe$area[i],
              cafe$produto[i],
              cafe$quantidade_por_metro[i],
              cafe$num_ruas[i],
              cafe$total_litros[i]))
}
cat('\nResumo estatístico para Café:\n')
cat('Média:', mean(as.numeric(cafe$total_litros)), '\n')
cat('Desvio padrão amostral:', sd(as.numeric(cafe$total_litros)), '\n')
