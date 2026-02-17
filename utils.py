import json

# Calcula o consumo em kWh de um aparelho
def calcular_consumo(potencia, horas_por_dia, dias):
    return (potencia * horas_por_dia * dias) / 1000


# Salva a lista de aparelhos em um arquivo JSON
def salvar_dados(aparelhos, arquivo="dados.json"):
    with open(arquivo, "w") as f:
        json.dump(aparelhos, f, indent=4)


# Carrega a lista de aparelhos de um arquivo JSON
def carregar_dados(arquivo="dados.json"):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []