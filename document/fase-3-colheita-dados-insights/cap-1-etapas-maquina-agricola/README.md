# 🌱 Projeto: Etapas de uma Máquina Agrícolae — Fase 3

**Nome do Grupo:** IA 2/2025  
**Integrantes:** 
- Gustavo Redoan
- Jorge Macedo
- Lucca Benigno

---
## Sumário

1. [Introdução](#introducao)
2. [Objetivo](#objetivo)
3. [Estrutura do Projeto](#projeto)
4. [Passo a Passo – Importação no Oracle](#importacao)
5. [Consultas SQL](#consultas)
6. [Resultados](#resultados)
7. [Conclusão](#conclusao)
8. [Licença](#licenca)

---
## <a name="introducao"></a>1. Introdução

Esta atividade tem como objetivo importar e analisar, no Oracle SQL Developer, os dados coletados pelos sensores do sistema de irrigação inteligente. O processo envolveu a criação da tabela SENSORES, configuração de tipos de dados e execução de consultas SQL para apoiar a análise de umidade, pH e estado do solo, consolidando o uso de banco de dados.

---
## <a name="objetivo"></a>2. Objetivo
- O objetivo desta atividade foi carregar os dados coletados pelos sensores na Fase 2 dentro de um banco de dados Oracle, realizar consultas SQL e documentar todo o processo no GitHub.

---
## <a name="projeto"></a>3. Estrutura do Projeto

```
.
└── projetos-faculdade
    └── assets    
        └── fase-3-cap-1-etapas-maquina-agricola-0.png
        └── fase-3-cap-1-etapas-maquina-agricola-1.png
        └── fase-3-cap-1-etapas-maquina-agricola-2.png
        └── fase-3-cap-1-etapas-maquina-agricola-3.png
        └── fase-3-cap-1-etapas-maquina-agricola-4.png
        └── fase-3-cap-1-etapas-maquina-agricola-5.png
        └── fase-3-cap-1-etapas-maquina-agricola-query-0.png
        └── fase-3-cap-1-etapas-maquina-agricola-query-1.png
        └── fase-3-cap-1-etapas-maquina-agricola-query-2.png
        └── fase-3-cap-1-etapas-maquina-agricola-query-3.png
        └── fase-3-cap-1-etapas-maquina-agricola-query-4.png
        └── fase-3-cap-1-etapas-maquina-agricola-query-5.png
    └── data 
        └── Sensores_fazenda.txt    
    └── document 
        └── README.md
    └── src 
        └── consultasSQL.txt
    └── README.md    

```
---
## <a name="importacao"></a>4. Passo a Passo – Importação no Oracle
- Etapa 1 – Início da Importação

No Oracle SQL Developer, clique com o botão direito sobre a conexão desejada (ex:FiapDevelopment) → Selecione "Tabelas" → "Importar Dados".

Exemplo:
<p align="center">
  <img src="../../../assets/fase-3-cap-1-etapas-maquina-agricola-0.png" alt="Fase 3 - Colheita de Dados e Insights - Dados valiosos e maduros" width="80%">
</p>

- Etapa 2 – Seleção do Arquivo

Escolha o arquivo de origem: data/Sensores_fazenda.txt

Origem: ../../../data

Codificação: UTF-8

Delimitador: ;

Cabeçalho: Sim

Exemplo:
<p align="center">
  <img src="../../../assets/fase-3-cap-1-etapas-maquina-agricola-1.png" alt="Fase 3 - Colheita de Dados e Insights - Dados valiosos e maduros" width="80%">
</p>


- Etapa 3 – Configuração da Tabela

Método de Importação: Inserir

Nome da Tabela: SENSORES

Exemplo:
<p align="center">
  <img src="../../../assets/fase-3-cap-1-etapas-maquina-agricola-2.png" alt="Fase 3 - Colheita de Dados e Insights - Dados valiosos e maduros" width="80%">
</p>

- Etapa 4 – Escolha de Colunas

Confirme as colunas que serão importadas (mantendo a ordem original): NPK, PH, EstadoPH, Umidade, NPK_OK, Chuva, BombaDagua

Exemplo:
<p align="center">
  <img src="../../../assets/fase-3-cap-1-etapas-maquina-agricola-3.png" alt="Fase 3 - Colheita de Dados e Insights - Dados valiosos e maduros" width="80%">
</p>


- Etapa 5 – Definição de Tipos de Dados

Ajuste os tipos de dados conforme necessário:

| Coluna     | Tipo de Dado | Observação        |
| ---------- | ------------ | ----------------- |
| NPK        | VARCHAR2(25) | valores numéricos |
| PH         | VARCHAR2(25) | valores decimais  |
| EstadoPH   | VARCHAR2(50) | texto             |
| Umidade    | NUMBER(5,2)  | numérico          |
| NPK_OK     | BOOLEAN      | verdadeiro/falso  |
| Chuva      | VARCHAR2(10) | ON/OFF            |
| BombaDagua | VARCHAR2(10) | ON/OFF            |

Exemplo:
<p align="center">
  <img src="../../../assets/fase-3-cap-1-etapas-maquina-agricola-4.png" alt="Fase 3 - Colheita de Dados e Insights - Dados valiosos e maduros" width="80%">
</p>


- Etapa 6 – Conclusão da Importação

Clique em Finalizar para criar a tabela e inserir os dados.

Exemplo:
<p align="center">
  <img src="../../../assets/fase-3-cap-1-etapas-maquina-agricola-4.png" alt="Fase 3 - Colheita de Dados e Insights - Dados valiosos e maduros" width="80%">
</p>

---

## <a name="importacao"></a>5. Carga de Dados no Oracle

Após a importação, os dados da tabela SENSORES foram carregados com sucesso.

Evidência de consulta:

SELECT * FROM SENSORES;

Tabela carregada:
<p align="center">
  <img src="../../../assets/fase-3-cap-1-etapas-maquina-agricola-query-0.png" alt="Fase 3 - Colheita de Dados e Insights - Dados valiosos e maduros" width="80%">
</p>

## <a name="consultas"></a>6. Consultas SQL

A seguir, as principais consultas realizadas no Oracle SQL Developer:

a) Contagem Total de Leituras

SELECT COUNT(*) AS total_leituras
FROM SENSORES;

b) Filtragem (WHERE)

SELECT *
FROM SENSORES
WHERE EstadoPH = 'Alcalino';

c) Ordenação (ORDER BY)

SELECT *
FROM SENSORES
ORDER BY Umidade DESC;

d) Estatísticas Simples (AVG, MAX, MIN)

SELECT 
    AVG(Umidade) AS media_umidade,
    MAX(Umidade) AS umidade_maxima,
    MIN(Umidade) AS umidade_minima
FROM SENSORES;

## <a name="resultados"></a>7. Resultados

As consultas mostraram que:

O total de leituras armazenadas: 87 registros

Os valores de umidade média e pH variam de acordo com o estado químico do solo.

O dataset representa medições de NPK, pH, umidade e status dos sensores (bomba, chuva) coletadas na Fase 2.

## <a name="conclusao"></a>8. Conclusão

O processo de importação e análise SQL foi concluído com sucesso.

Os dados do arquivo Sensores_fazenda.txt foram carregados no banco Oracle, permitindo realizar consultas, filtragens e estatísticas básicas para apoiar a gestão inteligente de irrigação e análise do solo.

## 📜 <a name="licenca"></a>8. Licença

Código educacional de uso livre. Adapte conforme sua necessidade acadêmica ou pessoal.