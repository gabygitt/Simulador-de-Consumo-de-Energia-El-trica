from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

# Gera um relatório em PDF, contendo tabela de consumo, gráfico e resumo dos aparelhos
def gerar_pdf(aparelhos, caminho, grafico_path):
    if not aparelhos:
        return

    doc = SimpleDocTemplate(caminho, pagesize=A4)
    elementos = []
    styles = getSampleStyleSheet()

    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    elementos.append(Paragraph("Relatório de Consumo de Energia", styles["Heading1"]))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"Gerado em: {data_atual}", styles["Normal"]))
    elementos.append(Spacer(1, 20))


    #TABELA
    dados_tabela = [["Aparelho", "Consumo (kWh)", "Custo (R$)"]]

    total = 0

    for a in aparelhos:
        dados_tabela.append([
            a["nome"],
            f"{a['consumo']:.2f}",
            f"{a['custo']:.2f}"
        ])
        total += a["consumo"]

    maior = max(aparelhos, key=lambda x: x["consumo"])

    tabela = Table(dados_tabela)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elementos.append(tabela)
    elementos.append(Spacer(1, 20))


    # GRÁFICO
    elementos.append(Paragraph("Gráfico de Consumo", styles["Heading2"]))
    elementos.append(Spacer(1, 10))
    elementos.append(Image(grafico_path, width=6*inch, height=3*inch))
    elementos.append(Spacer(1, 20))


    # RESUMO DO CONSUMO
    elementos.append(
        Paragraph(
            f"Maior consumo: {maior['nome']} ({maior['consumo']:.2f} kWh)",
            styles["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Consumo total mensal: {total:.2f} kWh",
            styles["Normal"]
        )
    )

    doc.build(elementos)
    return True