# Simulador de Consumo Elétrico

O Energy Dashboard é um sistema desenvolvido em Python com interface gráfica em Tkinter que permite simular o consumo mensal de energia elétrica residencial e tem como objetivo auxiliar no controle e na análise de gastos energéticos de forma simples e visual.

O sistema calcula:

- Consumo mensal em kWh
- Custo mensal com base na tarifa
- Aparelho com maior consumo
- Consumo total da residência
- Geração de relatório em PDF com gráfico e resumo

# Bibliotecas Utilizadas

## Interface Gráfica

* `tkinter` : criação da interface
* `PIL (Pillow)` : manipulação de imagens

## Gráficos

* `matplotlib` : geração de gráficos de barras

## Relatório

* `reportlab` : criação de PDF 

## Manipulação de Dados

* `json` : armazenamento em arquivo
* `datetime` : data e hora do relatório
* `os` : manipulação de arquivos

# Requisitos para Rodar o Sistema

- Ter Python instalado
- Instalar as bibliotecas necessárias
Abra o terminal na pasta do projeto e execute:

```bash
pip install matplotlib pillow reportlab
```

O `tkinter` já vem instalado com o Python.
