import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Função para exibir os planetas em uma tabela na interface gráfica
def exibir_planetas_gui(planetas, tree):
    for row in tree.get_children():
        tree.delete(row)
    for planeta in planetas:
        tree.insert('', 'end', values=(planeta['nome'], planeta['rotacao'], planeta['translacao'], planeta['diametro'], planeta['temperatura'], planeta['distancia'], planeta['imagem']))

# Função para carregar os planetas do arquivo JSON
def carregar_planetas():
    try:
        with open('planetas.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para salvar os planetas no arquivo JSON
def salvar_planetas(planetas):
    with open('planetas.json', 'w') as file:
        json.dump(planetas, file, indent=4)

# Função para adicionar um novo planeta
def cadastrar_planeta():
    def salvar():
        nome = nome_entry.get().strip()
        rotacao = rotacao_entry.get().strip()
        translacao = translacao_entry.get().strip()
        diametro = diametro_entry.get().strip()
        temperatura = temperatura_entry.get().strip()
        distancia = distancia_entry.get().strip()
        imagem = imagem_entry.get().strip()

        if not nome or not rotacao or not translacao or not diametro or not temperatura or not distancia or not imagem:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        planeta = {
            'id': str(os.urandom(4).hex()),
            'nome': nome,
            'rotacao': rotacao,
            'translacao': translacao,
            'diametro': diametro,
            'temperatura': temperatura,
            'distancia': distancia,
            'imagem': imagem
        }

        planetas = carregar_planetas()
        planetas.append(planeta)
        salvar_planetas(planetas)
        messagebox.showinfo("Sucesso", "Planeta cadastrado com sucesso!")
        janela_cadastrar.destroy()
        visualizar_planetas()

    janela_cadastrar = tk.Toplevel()
    janela_cadastrar.title("Cadastrar Novo Planeta")
    janela_cadastrar.geometry("400x300")
    janela_cadastrar.configure(bg="#f4f4f4")  # Background claro

    tk.Label(janela_cadastrar, text="Nome:", bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5)
    nome_entry = tk.Entry(janela_cadastrar)
    nome_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Rotação (h):", bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5)
    rotacao_entry = tk.Entry(janela_cadastrar)
    rotacao_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Translação (d):", bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5)
    translacao_entry = tk.Entry(janela_cadastrar)
    translacao_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Diâmetro (km):", bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5)
    diametro_entry = tk.Entry(janela_cadastrar)
    diametro_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Temperatura (°C):", bg="#f4f4f4").grid(row=4, column=0, padx=10, pady=5)
    temperatura_entry = tk.Entry(janela_cadastrar)
    temperatura_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Distância ao Sol (milhões de km):", bg="#f4f4f4").grid(row=5, column=0, padx=10, pady=5)
    distancia_entry = tk.Entry(janela_cadastrar)
    distancia_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Link da Imagem:", bg="#f4f4f4").grid(row=6, column=0, padx=10, pady=5)
    imagem_entry = tk.Entry(janela_cadastrar)
    imagem_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar, bg="#007bff", fg="white").grid(row=7, columnspan=2, pady=10)

# Função para visualizar planetas
def visualizar_planetas():
    planetas = carregar_planetas()
    exibir_planetas_gui(planetas, tree)

# Função para buscar um planeta
def buscar_planeta():
    search_term = busca_entry.get().strip().lower()
    planetas = carregar_planetas()
    resultados = [p for p in planetas if search_term in p['nome'].lower()]
    exibir_planetas_gui(resultados, tree)

# Função para editar um planeta
def editar_planeta():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um planeta para editar.")
        return

    id_planeta = tree.item(selected_item, 'values')[0]
    planetas = carregar_planetas()
    planeta = next((p for p in planetas if p['nome'] == id_planeta), None)

    def salvar_edicao():
        nome = nome_entry.get().strip()
        rotacao = rotacao_entry.get().strip()
        translacao = translacao_entry.get().strip()
        diametro = diametro_entry.get().strip()
        temperatura = temperatura_entry.get().strip()
        distancia = distancia_entry.get().strip()
        imagem = imagem_entry.get().strip()

        planeta.update({
            'nome': nome or planeta['nome'],
            'rotacao': rotacao or planeta['rotacao'],
            'translacao': translacao or planeta['translacao'],
            'diametro': diametro or planeta['diametro'],
            'temperatura': temperatura or planeta['temperatura'],
            'distancia': distancia or planeta['distancia'],
            'imagem': imagem or planeta['imagem']
        })

        salvar_planetas(planetas)
        messagebox.showinfo("Sucesso", "Planeta atualizado com sucesso!")
        janela_editar.destroy()
        visualizar_planetas()

    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Planeta")
    janela_editar.geometry("400x300")
    janela_editar.configure(bg="#f4f4f4")

    tk.Label(janela_editar, text="Nome:", bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5)
    nome_entry = tk.Entry(janela_editar, text=planeta['nome'])
    nome_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_editar, text="Rotação (h):", bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5)
    rotacao_entry = tk.Entry(janela_editar, text=planeta['rotacao'])
    rotacao_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_editar, text="Translação (d):", bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5)
    translacao_entry = tk.Entry(janela_editar, text=planeta['translacao'])
    translacao_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_editar, text="Diâmetro (km):", bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5)
    diametro_entry = tk.Entry(janela_editar, text=planeta['diametro'])
    diametro_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_editar, text="Temperatura (°C):", bg="#f4f4f4").grid(row=4, column=0, padx=10, pady=5)
    temperatura_entry = tk.Entry(janela_editar, text=planeta['temperatura'])
    temperatura_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_editar, text="Distância ao Sol (milhões de km):", bg="#f4f4f4").grid(row=5, column=0, padx=10, pady=5)
    distancia_entry = tk.Entry(janela_editar, text=planeta['distancia'])
    distancia_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_editar, text="Link da Imagem:", bg="#f4f4f4").grid(row=6, column=0, padx=10, pady=5)
    imagem_entry = tk.Entry(janela_editar, text=planeta['imagem'])
    imagem_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Button(janela_editar, text="Salvar", command=salvar_edicao, bg="#007bff", fg="white").grid(row=7, columnspan=2, pady=10)

# Função para deletar um planeta
def deletar_planeta():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um planeta para excluir.")
        return

    id_planeta = tree.item(selected_item, 'values')[0]
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este planeta?"):
        planetas = carregar_planetas()
        planetas = [p for p in planetas if p['nome'] != id_planeta]
        salvar_planetas(planetas)
        messagebox.showinfo("Sucesso", "Planeta excluído com sucesso!")
        visualizar_planetas()

# Função principal
def menu_gui():
    root = tk.Tk()
    root.title("Sistema de Cadastro de Planetas do Sistema Solar")
    root.geometry("800x500")
    root.configure(bg="#f4f4f4")  # Cor de fundo leve

    global tree
    tree = ttk.Treeview(root, columns=("Nome", "Rotação", "Translação", "Diâmetro", "Temperatura", "Distância", "Imagem"), show="headings", height=10)
    tree.heading("Nome", text="Nome")
    tree.heading("Rotação", text="Rotação (h)")
    tree.heading("Translação", text="Translação (d)")
    tree.heading("Diâmetro", text="Diâmetro (km)")
    tree.heading("Temperatura", text="Temperatura (°C)")
    tree.heading("Distância", text="Distância ao Sol (milhões km)")
    tree.heading("Imagem", text="Imagem")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=x_scrollbar.set)

    tk.Label(root, text="Buscar Planeta:", bg="#f4f4f4").pack(side=tk.LEFT, padx=5, pady=5)
    global busca_entry
    busca_entry = ttk.Entry(root)
    busca_entry.pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="Buscar", command=buscar_planeta, bg="#007bff", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="Cadastrar", command=cadastrar_planeta, bg="#28a745", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="Editar", command=editar_planeta, bg="#ffc107", fg="black").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="Excluir", command=deletar_planeta, bg="#dc3545", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="Visualizar Todos", command=visualizar_planetas, bg="#007bff", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="Sair", command=root.quit, bg="#6c757d", fg="white").pack(side=tk.LEFT, padx=5, pady=5)

    visualizar_planetas()

    root.mainloop()

if __name__ == "__main__":
    menu_gui()
