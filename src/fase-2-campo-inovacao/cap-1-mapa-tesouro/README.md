# 🌱 Projeto: Sistema de Irrigação Inteligente — Fase 2
### Curso: Campo Inovação | FarmTech Solutions
**Nome do Grupo:** IA 2/2025  
**Integrantes:** Gustavo 

**Microcontrolador:** ESP32  
**Simulação:** [Wokwi.com](https://wokwi.com)  
**Framework:** Arduino (PlatformIO)  

---
## 🧭 Introdução

Este projeto apresenta um protótipo de sistema de irrigação inteligente que combina leituras de sensores com regras de decisão para controlar uma bomba de água. O objetivo é demonstrar, em ambiente simulado (Wokwi) e com código para ESP32, como sinais ambientais e inputs de usuário podem ser integrados para automatizar decisões de manejo agrícola.

## 🔍 Visão Geral do Projeto

### Objetivos
- Automatizar a irrigação considerando umidade do solo, simulação de nutrientes (NPK), pH simulado e previsão de chuva via comando serial.
- Fornecer exemplo didático de integração hardware-software para aplicações de IoT agrícola.

### Metodologia
- Projeto e simulação do circuito no Wokwi.
- Implementação do firmware em C++ (PlatformIO/Arduino) para ESP32.
- Testes funcionais via Serial Monitor e simulações controladas.

---
## 🎯 Objetivo do Projeto

Desenvolver um **sistema de irrigação automatizado e inteligente**, capaz de:

1. **Monitorar a umidade do solo** em tempo real via sensor DHT22.  
2. **Simular os nutrientes NPK (Nitrogênio, Fósforo e Potássio)** por meio de 3 botões físicos.  
3. **Simular o pH da terra** com um sensor **LDR**, convertendo o valor lido (0–4095) em escala de **pH (0–14)**.  
4. **Controlar automaticamente a bomba de água**, ligada a um **relé**, seguindo regras ambientais.  
5. **Permitir controle manual de “chuva”** via **Monitor Serial**, imitando a integração com uma API meteorológica.  

---

## ⚙️ Funcionamento Geral

O sistema faz leituras contínuas dos sensores e decide **ligar ou desligar a bomba de irrigação** com base nas seguintes condições:

| Condição | Descrição | Requisito |
|-----------|------------|-----------|
| **NPK_OK** | Todos os três botões (N, P e K) estão pressionados (estado lógico 1). | ✅ Todos ON |
| **pH Neutro** | O valor lido pelo LDR convertido está entre **6.9 e 7.1**. | ✅ Faixa neutra |
| **Umidade baixa** | O valor de umidade lido pelo DHT22 é **menor que 40%**. | ✅ Solo seco |
| **Sem chuva prevista** | O usuário digita `chuva=false` no Serial Monitor. | ✅ Sem bloqueio de chuva |

> 💧 **A bomba só liga se todas as condições forem verdadeiras simultaneamente.**  
> Se qualquer uma deixar de ser verdadeira, a bomba desliga automaticamente.

---

## 💡 Lógica de Controle

```cpp
bool liga = (NPK_OK && ph_neutro && humidity_low && !chuva);
```

| Variável | Significado | Tipo |
|-----------|-------------|------|
| `NPK_OK` | Todos os botões de nutrientes estão ativos | bool |
| `ph_neutro` | Valor do pH entre 6.9 e 7.1 | bool |
| `humidity_low` | Umidade abaixo de 40% | bool |
| `chuva` | Previsão de chuva informada pelo usuário (`true` = chovendo) | bool |

---

## 🌤️ Controle de Chuva via Monitor Serial

O sistema aceita comandos digitados diretamente no **Monitor Serial (115200 baud)**:

| Comando | Efeito |
|----------|---------|
| `chuva=true` | Indica **previsão de chuva** → desliga bomba automaticamente |
| `chuva=false` | Indica **tempo seco** → libera irrigação novamente |

> ⚙️ Configure o *Line Ending* como **Newline (\n)** no Serial Monitor.

### Exemplo de resposta:
```
Previsão de chuva recebida → irrigação bloqueada.
```

---

## 🧩 Componentes Utilizados

<p align="center">
  <img src="https://github.com/user-attachments/assets/fase-2-campo-inovacao-cap1-mapa-tesouro.png" alt="Mapa do Tesouro - Fase 2" width="80%">
</p>


| Componente | Função | Pino ESP32 |
|-------------|--------|-------------|
| DHT22 | Sensor de temperatura/umidade | 15 |
| LDR | Simula sensor de pH (0–14) | 34 (ADC) |
| Botão N | Nitrogênio | 13 |
| Botão P | Fósforo | 12 |
| Botão K | Potássio | 14 |
| LED vermelho | Simula relé da bomba d’água | 26 |

---

## 🧱 Estrutura do Projeto

```
├── cap1-mapa-tesouro/
    └── main.cpp              # Código principal do sistema
    └── diagram.json          # Diagrama do circuito no Wokwi
    └── README.md             # Documentação do projeto

```

---

## 🔌 Diagrama de Ligação (Wokwi)

Os componentes estão conectados conforme o arquivo `diagram.json`:

- **Botões (N, P, K):** pinos 13, 12 e 14 (com `INPUT_PULLUP`)
- **LDR:** pino 34 (ADC)
- **DHT22:** pino 15 (dados)
- **LED vermelho (bomba):** pino 26 (saída digital)

### 📘 Uso no Wokwi
1. Clique em ▶️ **Start Simulation**
2. Abra o **Serial Monitor**
3. Digite:
   ```
   chuva=true
   ```
   ou  
   ```
   chuva=false
   ```
4. Observe o LED vermelho acendendo/apagando conforme as condições de irrigação.

---

## 🔬 Exemplo de Saída no Serial

```
N P K | pH | Estado(pH) | Umid(%) | NPK_OK | Chuva | Bomba
1 1 1 | 7.00 | Neutro | 35.2 | SIM | NAO | ON
```
➡️ **Bomba ligada** (chuva=false, pH neutro, NPK ativos e solo seco)

```
chuva=true
Previsão de chuva recebida → irrigação bloqueada.
1 1 1 | 7.00 | Neutro | 35.2 | SIM | SIM | OFF
```
➡️ **Bomba desligada automaticamente** por previsão de chuva.

---

## 📋 Requisitos do Ambiente

- **Placa:** ESP32 DevKit V1  
- **Bibliotecas:**
  - `DHT sensor library` — leitura do sensor DHT22  
  - `Adafruit Unified Sensor` — suporte à lib DHT  

Instalação automática via PlatformIO (`platformio.ini` já configurado).

---

## 🧠 Possíveis Extensões Futuras

- Integração real com API meteorológica (OpenWeather API via Python ou ESP32 WiFi).  
- Dashboard web para monitorar dados (umidade, pH, irrigação, chuva).  
- Ajuste dinâmico de limiares conforme cultura agrícola.  

---

## 📜 Licença

Código educacional de uso livre. Adapte conforme sua necessidade acadêmica ou pessoal.
