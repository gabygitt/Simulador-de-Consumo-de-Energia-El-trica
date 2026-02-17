import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from utils import calcular_consumo, salvar_dados, carregar_dados
from relatorio import gerar_pdf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os


# CORES
BG_PRINCIPAL = "#4D4965"
ROXO_CARD = "#2A1E40"
ROXO_BOTAO = "#6A0DAD"
ROXO_DESTAQUE = "#9D4EDD"
TEXTO = "#FFFFFF"


# JANELA
root = tk.Tk()
root.title("Simulador de Consumo de Energia Residencial")
root.geometry("1100x750")
root.configure(bg=BG_PRINCIPAL)


# CARREGAR E REDIMENSIONAR ÍCONES
def carregar_icone(nome, tamanho=(24, 24)):
    caminho = os.path.join("icons", nome)
    img = Image.open(caminho)
    img = img.resize(tamanho)
    return ImageTk.PhotoImage(img)

icon_add = carregar_icone("add.png")
icon_calendar = carregar_icone("calendar.png")
icon_clock = carregar_icone("clock.png")
icon_trash = carregar_icone("trash.png")
icon_lamp = carregar_icone("lamp.png")
icon_lightning = carregar_icone("lightning.png")
icon_money = carregar_icone("money.png")


# HEADER
header = tk.Frame(root, bg=BG_PRINCIPAL)
header.pack(pady=35)

tk.Label(
    header,
    text="⚡ Energy Dashboard",
    bg=BG_PRINCIPAL,
    fg="black",
    font=("Muthiara -Demo Version-", 40)
).pack()

tk.Label(
    header,
    text="-- Simulador inteligente de consumo elétrico residencial --",
    bg=BG_PRINCIPAL,
    fg="white",
    font=("Ebrima", 13)
).pack(pady=(5, 0))


# DADOS
aparelhos = carregar_dados()


# FUNÇÕES
def adicionar():
    #Coleta os dados, calcula consumo e custo do aparelho e adiciona à lista salvando no JSON
    try:
        nome = entry_nome.get()
        potencia = float(entry_potencia.get())
        horas = float(entry_horas.get())
        dias = int(entry_dias.get())
        tarifa = float(entry_tarifa.get())

        consumo = calcular_consumo(potencia, horas, dias)
        custo = consumo * tarifa

        aparelhos.append({
            "nome": nome,
            "consumo": consumo,
            "custo": custo
        })

        salvar_dados(aparelhos)
        atualizar_texto()
        atualizar_grafico()
        limpar_campos()

    except:
        messagebox.showerror("Erro", "Preencha corretamente os campos.")


# Limpa todos os campos do formulário após a inserção de um aparelho
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_potencia.delete(0, tk.END)
    entry_horas.delete(0, tk.END)
    entry_dias.delete(0, tk.END)
    entry_tarifa.delete(0, tk.END)

# Limpa todos os campos do formulário após a inserção de um aparelho
def limpar_dados():
    aparelhos.clear()
    salvar_dados(aparelhos)
    atualizar_texto()
    atualizar_grafico()

# Atualiza a área de resultados, exibindo os aparelhos, o maior consumo e o total mensal
def atualizar_texto():
    resultado.config(state="normal")
    resultado.delete(1.0, tk.END)

    if not aparelhos:
        resultado.insert(tk.END, "Nenhum aparelho cadastrado.")
        resultado.config(state="disabled")
        return

    total = 0

    for a in aparelhos:
        resultado.insert(
            tk.END,
            f"{a['nome']} → {a['consumo']:.2f} kWh | R$ {a['custo']:.2f}\n"
        )
        total += a["consumo"]

    maior = max(aparelhos, key=lambda x: x["consumo"])

    resultado.insert(tk.END, "\n---------------------------\n")
    resultado.insert(
        tk.END,
        f"🔥 Maior consumo: {maior['nome']} ({maior['consumo']:.2f} kWh)\n"
    )
    resultado.insert(
        tk.END,
        f"⚡ Total: {total:.2f} kWh"
    )

    resultado.config(state="disabled")

def atualizar_grafico():
    ax.clear()
    ax.set_facecolor(BG_PRINCIPAL)

    if aparelhos:
        nomes = [a["nome"] for a in aparelhos]
        consumos = [a["consumo"] for a in aparelhos]

        bars = ax.bar(nomes, consumos)

        for bar in bars:
            bar.set_color(ROXO_DESTAQUE)

        ax.set_title("Consumo por Aparelho", color="white", fontsize=12)
        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("white")

    fig.patch.set_facecolor(BG_PRINCIPAL)
    canvas.draw()


# Gera o relatório em PDF, salvando o gráfico temporariamente e removendo-o após a criação do arquivo
def baixar_pdf():
    if not aparelhos:
        messagebox.showwarning("Aviso", "Não há dados para gerar o relatório.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF", "*.pdf")]
    )

    if not caminho:
        return

    # Salva gráfico temporiamente
    grafico_path = "grafico_temp.png"
    fig.savefig(grafico_path)

    sucesso = gerar_pdf(aparelhos, caminho, grafico_path)

    # Remove o arquivo temporário
    if os.path.exists(grafico_path):
        os.remove(grafico_path)

    if sucesso:
        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")



# FORMULÁRIO
form = tk.Frame(root, bg=ROXO_CARD, padx=30, pady=25)
form.pack(pady=20)

def criar_label(texto, linha, icone=None):
    frame_label = tk.Frame(form, bg=ROXO_CARD)
    frame_label.grid(row=linha, column=0, sticky="w", pady=10)

    if icone:
        tk.Label(frame_label, image=icone, bg=ROXO_CARD).pack(side="left", padx=6)

    tk.Label(
        frame_label,
        text=texto,
        bg=ROXO_CARD,
        fg=TEXTO,
        font=("Ebrima", 11, "bold")
    ).pack(side="left")

def criar_entry(linha):
    e = tk.Entry(
        form,
        width=28,
        font=("Ebrima", 11),
        bg="#3A2E55",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    e.grid(row=linha, column=1, pady=10, padx=10)
    return e

criar_label("Tarifa (R$/kWh):", 0, icon_money)
entry_tarifa = criar_entry(0)

criar_label("Nome do aparelho:", 1, icon_lamp)
entry_nome = criar_entry(1)

criar_label("Potência (W):", 2, icon_lightning)
entry_potencia = criar_entry(2)

criar_label("Horas por dia:", 3, icon_clock)
entry_horas = criar_entry(3)

criar_label("Dias por mês:", 4, icon_calendar)
entry_dias = criar_entry(4)


# BOTÕES
btn_frame = tk.Frame(root, bg=BG_PRINCIPAL)
btn_frame.pack(pady=20)

tk.Button(
    btn_frame,
    text=" Adicionar",
    image=icon_add,
    compound="left",
    bg=ROXO_BOTAO,
    fg="white",
    font=("Ebrima", 11, "bold"),
    padx=20,
    pady=10,
    relief="flat",
    cursor="hand2",
    command=adicionar
).pack(side="left", padx=15)

tk.Button(
    btn_frame,
    text=" Limpar Dados",
    image=icon_trash,
    compound="left",
    bg="#B00020",
    fg="white",
    font=("Ebrima", 11, "bold"),
    padx=20,
    pady=10,
    relief="flat",
    cursor="hand2",
    command=limpar_dados
).pack(side="left", padx=15)

tk.Button(
    btn_frame,
    text=" Baixar PDF",
    bg="#2E7D32",
    fg="white",
    font=("Ebrima", 11, "bold"),
    padx=20,
    pady=10,
    relief="flat",
    cursor="hand2",
    command=baixar_pdf
).pack(side="left", padx=15)


# RESULTADO
resultado = tk.Text(
    root,
    width=85,
    height=8,
    bg=ROXO_CARD,
    fg="white",
    insertbackground="white",
    font=("Ebrima", 11),
    relief="flat"
)
resultado.pack(pady=20)
resultado.config(state="disabled")


# GRÁFICO
fig, ax = plt.subplots(figsize=(8, 4)) # Estrutura do gráfico
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack() # Mostra visualmente o gráfico na tela

atualizar_texto()
atualizar_grafico()

root.mainloop()