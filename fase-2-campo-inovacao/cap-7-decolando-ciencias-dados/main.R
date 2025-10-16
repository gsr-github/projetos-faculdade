# Carregar pacotes
library(readxl)
library(dplyr)
library(ggplot2)
library(rlang)   

# Ler a planilha
df <- read_excel("c:\\<path>\\base_agro_educacional.xlsx") %>%
  mutate(
    Producao_Toneladas   = as.numeric(Producao_Toneladas),
    Numero_Trabalhadores = as.numeric(Numero_Trabalhadores)
  )

# Visualizar estrutura
str(df)

# Filtrar NAs para cálculos
df_num <- df %>% filter(!is.na(Producao_Toneladas))

# 3. Escolha uma variável quantitativa e faça uma análise exploratória dela em R contendo
media   <- mean(df_num$Producao_Toneladas, na.rm = TRUE)
mediana <- median(df_num$Producao_Toneladas, na.rm = TRUE)

# Moda robusta (lida com empates)
tab <- sort(table(df_num$Producao_Toneladas), decreasing = TRUE)
moda_vals <- as.numeric(names(tab)[tab == max(tab)])

cat("Média:", media, "\n")
cat("Mediana:", mediana, "\n")
cat("Moda:", paste(moda_vals, collapse = ", "), "\n")

# ---- Medidas de Dispersão ----
variancia     <- var(df_num$Producao_Toneladas, na.rm = TRUE)
desvio_padrao <- sd(df_num$Producao_Toneladas, na.rm = TRUE)
amplitude     <- max(df_num$Producao_Toneladas, na.rm = TRUE) - min(df_num$Producao_Toneladas, na.rm = TRUE)
coef_var      <- (desvio_padrao / media) * 100

cat("Variância:", variancia, "\n")
cat("Desvio Padrão:", desvio_padrao, "\n")
cat("Amplitude:", amplitude, "\n")
cat("Coeficiente de Variação (%):", coef_var, "\n")

# ---- Medidas Separatrizes ----
quartis    <- quantile(df_num$Producao_Toneladas, probs = c(0.25, 0.5, 0.75), na.rm = TRUE)
decis      <- quantile(df_num$Producao_Toneladas, probs = seq(0.1, 0.9, 0.1), na.rm = TRUE)
percentis  <- quantile(df_num$Producao_Toneladas, probs = seq(0.01, 0.99, 0.01), na.rm = TRUE)

cat("Quartis:\n");    print(quartis)
cat("Decis:\n");      print(decis)
cat("Percentis:\n");  print(percentis)

# ---- Análise gráfica ----

g1 <- ggplot(df, aes(x = Producao_Toneladas, y = Numero_Trabalhadores)) +
  stat_summary_bin(
    fun = "mean", geom = "col",
    bins = 10, fill = "skyblue", color = "black", na.rm = TRUE
  ) +
  stat_summary_bin(
    fun = "mean", geom = "text",
    aes(label = round(after_stat(y), 1)),
    bins = 10, vjust = -0.3, size = 3.5, na.rm = TRUE
  ) +
  geom_vline(xintercept = media,   color = "red",       linetype = "dashed", linewidth = 1) +
  geom_vline(xintercept = mediana, color = "darkgreen", linetype = "dashed", linewidth = 1) +
  annotate("text", x = media, y = Inf, vjust = 2,
           label = paste0("Média = ", round(media, 2)),
           color = "red", fontface = "bold") +
  annotate("text", x = mediana, y = Inf, vjust = 4,
           label = paste0("Mediana = ", round(mediana, 2)),
           color = "darkgreen", fontface = "bold") +
  labs(
    title = "Média de Trabalhadores por Faixa de Produção (Toneladas)",
    subtitle = "Linhas tracejadas: Média (vermelha) e Mediana (verde)",
    x = "Produção (Toneladas)",
    y = "Média de Trabalhadores"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.title = element_text(face = "bold", hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5)
  ) +
  expand_limits(y = 0) +
  scale_y_continuous(expand = expansion(mult = c(0.02, 0.10)))

print(g1)

# 4. Escolha uma variável qualitativa e faça uma análise gráfica dela em R. ----
var_qual <- "Tipo_Cultura"

g2 <- ggplot(df, aes(x = .data[[var_qual]])) +
  geom_bar(fill = "skyblue", color = "black", na.rm = TRUE) +
  geom_text(
    stat = "count",
    aes(label = ..count..),
    vjust = -0.3, size = 4
  ) +
  labs(
    title = "Distribuição por Tipo de Cultura",
    subtitle = "Contagem por categoria",
    x = "Tipo de Cultura",
    y = "Frequência"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.title = element_text(face = "bold", hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5)
  ) +
  expand_limits(y = 0) +
  scale_y_continuous(expand = expansion(mult = c(0.02, 0.10)))

print(g2)
