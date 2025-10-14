library(httr)
library(jsonlite)

# Coordenadas de exemplo (Belo Horiznte, Brasil)
latitude <- -19.55
longitude <- -43.56

# Coordenadas de exemplo (São Paulo, Brasil)
# latitude <- -23.54
# longitude <- -46.63

# Coordenadas de exemplo (Brasilia, Brasil)
# latitude <- -15.78
# longitude <- -47.92

# URL da API Open-Meteo
url <- paste0("https://api.open-meteo.com/v1/forecast?latitude=", latitude,
              "&longitude=", longitude, "&current_weather=true")

res <- GET(url)
data <- fromJSON(content(res, "text"))

if (!is.null(data$current_weather)) {
  weather <- data$current_weather
  cat("Temperatura:", weather$temperature, "°C\n")
  cat("Velocidade do vento:", weather$windspeed, "km/h\n")
  cat("Direção do vento:", weather$winddirection, "°\n")
} else {
  cat("Não foi possível obter os dados meteorológicos.\n")
}