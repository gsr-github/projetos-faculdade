# 🌾 Análise Exploratória de Dados Agropecuários (R)

**Grupo:** IA 2/2025  
**Integrante:** Gustavo  

---

## 📘 Introdução  

Este projeto tem como objetivo aplicar técnicas de **Estatística Descritiva** e **Análise Exploratória de Dados (EDA)** sobre uma base de dados agropecuária construída a partir de fontes públicas (CONAB, IBGE, MAPA, Embrapa, etc.).  

A análise foi realizada em linguagem **R**, utilizando os pacotes `readxl`, `dplyr` e `ggplot2` para leitura, manipulação e visualização dos dados contidos no arquivo **`base_agro_educacional.xlsx`**.  

---

## 🌱 Visão Geral do Projeto  

O estudo busca compreender o comportamento das variáveis agrícolas — principalmente **Produção (Toneladas)** e **Número de Trabalhadores** — através de medidas estatísticas e gráficos interpretativos.  

Foram aplicadas técnicas de:
- Medidas de **tendência central** (média, mediana e moda);
- Medidas de **dispersão** (variância, desvio padrão, amplitude e coeficiente de variação);
- **Medidas separatrizes** (quartis, decis e percentis);
- **Análise gráfica** para variáveis **quantitativas** e **qualitativas**.  

O código foi estruturado para seguir o fluxo de análise completo: **importação → tratamento → cálculo → visualização**.  

---

## 🧠 Estrutura do Código  

1. **Carregamento de Pacotes**
   ```r
   library(readxl)
   library(dplyr)
   library(ggplot2)
   library(rlang)
   ```

2. **Leitura da Base de Dados**
   - A planilha `base_agro_educacional.xlsx` é importada e as variáveis numéricas são convertidas para `numeric`.
   - O código remove valores ausentes (`NA`) para garantir a consistência dos cálculos.

3. **Medidas de Tendência Central**
   - Média, Mediana e Moda da variável **Producao_Toneladas**.
   - A moda foi tratada de forma robusta, suportando múltiplos valores com frequência máxima.

4. **Medidas de Dispersão**
   - Variância, Desvio Padrão, Amplitude e Coeficiente de Variação (%).
   - Avaliam o grau de variação em torno da média.

5. **Medidas Separatrizes**
   - Cálculo dos **quartis**, **decis** e **percentis**, fornecendo a posição relativa de cada observação.

6. **Análises Gráficas**
   - Gráfico 1: Relação entre **Produção (Toneladas)** e **Número de Trabalhadores**.  
     Inclui médias e linhas verticais representando a **média (vermelha)** e **mediana (verde)**.
   - Gráfico 2: Distribuição da variável **Tipo_Cultura**, com contagem de frequência por categoria.

---

## 📊 Visualizações  

### 🔹 Gráfico 1 — Média de Trabalhadores por Faixa de Produção
Representa a média de trabalhadores em diferentes faixas de produção.

```r
ggplot(df, aes(x = Producao_Toneladas, y = Numero_Trabalhadores)) +
  stat_summary_bin(fun = "mean", geom = "col", bins = 10, fill = "skyblue") +
  geom_vline(xintercept = media, color = "red", linetype = "dashed") +
  geom_vline(xintercept = mediana, color = "darkgreen", linetype = "dashed") +
  labs(
    title = "Média de Trabalhadores por Faixa de Produção (Toneladas)",
    subtitle = "Linhas tracejadas: Média (vermelha) e Mediana (verde)",
    x = "Produção (Toneladas)",
    y = "Média de Trabalhadores"
  )
```

🔸 **Interpretação:**  
O gráfico mostra como o número médio de trabalhadores varia conforme a produção aumenta, destacando as linhas de **média e mediana** para análise de simetria.

---

### 🔹 Gráfico 2 — Distribuição por Tipo de Cultura
Apresenta a contagem de registros por categoria de cultura agrícola.

```r
ggplot(df, aes(x = Tipo_Cultura)) +
  geom_bar(fill = "skyblue", color = "black") +
  geom_text(stat = "count", aes(label = ..count..), vjust = -0.3) +
  labs(
    title = "Distribuição por Tipo de Cultura",
    subtitle = "Contagem por categoria",
    x = "Tipo de Cultura",
    y = "Frequência"
  )
```

🔸 **Interpretação:**  
Permite observar quais tipos de cultura são mais representativos na base de dados, evidenciando a diversidade ou concentração produtiva.

---

## 📈 Resultados e Indicadores  

| Métrica | Descrição | Interpretação |
|----------|------------|----------------|
| **Média** | Valor médio da produção (toneladas) | Representa a tendência central |
| **Mediana** | Valor central da distribuição | Divide a amostra em 50% inferiores e superiores |
| **Moda** | Valor mais frequente | Identifica a produção típica |
| **Desvio Padrão** | Grau de dispersão | Mede variação em torno da média |
| **Coef. Variação (%)** | (Desvio padrão / Média) × 100 | Expressa variabilidade relativa |
| **Quartis / Decis / Percentis** | Divisões da distribuição | Mostram a posição relativa das observações |

---

## 🧾 Requisitos  

- **R versão 4.3+**
- Pacotes:
  ```r
  install.packages(c("readxl", "dplyr", "ggplot2", "rlang"))
  ```

---

## 🧪 Execução  

1. Salve o script como `analise_agro.R`
2. Execute no RStudio ou terminal:
   ```r
   source("analise_agro.R")
   ```
3. Certifique-se de ajustar o caminho da planilha:
   ```r
   "c:\<path>\base_agro_educacional.xlsx"
   ```

---

## 📂 Estrutura do Projeto  

```
.
├── analise_agro.R                # Script principal de análise
├── base_agro_educacional.xlsx    # Base de dados (entrada)
└── resultados/                   # Pasta opcional para salvar gráficos e saídas
```

---

## 📜 Conclusão  

O projeto fornece uma **análise estatística completa e visualmente intuitiva** da produção agrícola e sua relação com o número de trabalhadores.  
A partir das medidas e gráficos, é possível **identificar padrões, tendências e variações**, fundamentais para a tomada de decisão no setor agropecuário.

---

## 📄 Licença  

Uso educacional e livre para fins acadêmicos (FIAP — Fase 2: Campo Inovação).  
