import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import json
import os
import sys
from tkcalendar import Calendar

# --- Caminho de arquivos para funcionar no executável ---
def recurso_caminho(relativo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)

USUARIOS_FILE = recurso_caminho("usuarios.json")

# Criar arquivo JSON se não existir
if not os.path.exists(USUARIOS_FILE):
    with open(USUARIOS_FILE, "w") as f:
        json.dump([], f)

def carregar_usuarios():
    with open(USUARIOS_FILE, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def salvar_usuario(nome, usuario, email, senha, cargo="Aluno"):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario:
            return False, "Nome de usuário já existe."
        if u["email"] == email:
            return False, "E-mail já cadastrado."
    usuarios.append({
        "nome": nome,
        "usuario": usuario,
        "email": email,
        "senha": senha,
        "cargo": cargo
    })
    salvar_usuarios(usuarios)
    return True, "Usuário cadastrado com sucesso!"

def main_screen(nome, cargo, email):
    root = tk.Tk()
    root.title("Plataforma Educacional")
    root.state('zoomed')

    try:
        fundo_img = Image.open(recurso_caminho("Imagens/22.png"))
        fundo_img = fundo_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        fundo = ImageTk.PhotoImage(fundo_img)
    except Exception:
        fundo = None

    if fundo:
        label_fundo = tk.Label(root, image=fundo)
        label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    header = tk.Frame(root, bg="#353b44", height=80)
    header.pack(fill="x")
    title = tk.Label(header, text="Tsuki Education Systems", font=("Arial", 20), bg="#353b44", fg="white")
    title.pack(pady=20)

    welcome = tk.Label(root, text=f"Bem-vindo(a), {nome} ({cargo})", font=("Arial", 16), bg="#fffbfb")
    welcome.pack(pady=20)

    btn_frame = tk.Frame(root, bg="#f5f5f5")
    btn_frame.pack(pady=10)

    def ver_documentos():
        doc_win = tk.Toplevel(root)
        doc_win.title("Documentos do Aluno")
        doc_win.geometry("300x150")
        doc_win.configure(bg="#f5f5f5")
        tk.Label(doc_win, text="Informações do Usuário", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)
        tk.Label(doc_win, text=f"Nome: {nome}", font=("Arial", 14), bg="#f5f5f5").pack(pady=5)
        tk.Label(doc_win, text=f"E-mail: {email}", font=("Arial", 14), bg="#f5f5f5").pack(pady=5)

    def ver_desempenho():
        messagebox.showinfo("Desempenho", "Aqui será exibido o desempenho do aluno.")

    def aulas():
        aulas_win = tk.Toplevel(root)
        aulas_win.title("Aulas ao Vivo")
        aulas_win.geometry("700x500")
        aulas_win.configure(bg="#f5f5f5")

        tk.Label(aulas_win, text="Grade de Aulas ao Vivo - Ensino Médio (Manhã)", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

        colunas = ("Dia", "Horário", "Disciplina")
        tree = ttk.Treeview(aulas_win, columns=colunas, show="headings", height=15)
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        grade = [
            ("Segunda", "07:00 - 07:50", "Matemática"),
            ("Segunda", "07:50 - 08:40", "Português"),
            ("Segunda", "08:40 - 09:30", "História"),
            ("Terça", "07:00 - 07:50", "Geografia"),
            ("Terça", "07:50 - 08:40", "Química"),
            ("Terça", "08:40 - 09:30", "Física"),
            ("Quarta", "07:00 - 07:50", "Biologia"),
            ("Quarta", "07:50 - 08:40", "Educação Física"),
            ("Quarta", "08:40 - 09:30", "Matemática"),
            ("Quinta", "07:00 - 07:50", "Filosofia"),
            ("Quinta", "07:50 - 08:40", "História"),
            ("Quinta", "08:40 - 09:30", "Português"),
            ("Sexta", "07:00 - 07:50", "Sociologia"),
            ("Sexta", "07:50 - 08:40", "Geografia"),
            ("Sexta", "08:40 - 09:30", "Artes")
        ]

        for aula in grade:
            tree.insert("", "end", values=aula)

        tree.pack(pady=20, expand=True, fill="both")

    def calendario():
        cal_win = tk.Toplevel(root)
        cal_win.title("Calendário")
        cal_win.geometry("400x400")
        cal_win.configure(bg="#f5f5f5")
        tk.Label(cal_win, text="Calendário", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)
        cal = Calendar(cal_win, selectmode='day', year=2025, month=5, day=21)
        cal.pack(pady=20, expand=True, fill='both')

        def pegar_data():
            data = cal.get_date()
            messagebox.showinfo("Data Selecionada", f"Você selecionou: {data}")

        tk.Button(cal_win, text="Mostrar Data Selecionada", command=pegar_data, bg="#4a7abc", fg="white").pack(pady=10)

    def calcular_media():
        media_win = tk.Toplevel(root)
        media_win.title("Calculadora de Média")
        media_win.geometry("400x400")
        media_win.configure(bg="#f5f5f5")

        tk.Label(media_win, text="Calcular Média Final", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        def criar_entrada(rotulo):
            frame = tk.Frame(media_win, bg="#f5f5f5")
            frame.pack(pady=10)
            tk.Label(frame, text=rotulo, width=15, anchor="w", bg="#f5f5f5").pack(side="left")
            entrada = tk.Entry(frame, width=10)
            entrada.pack(side="left")
            return entrada

        entrada_prova1 = criar_entrada("Nota Prova 1:")
        entrada_prova2 = criar_entrada("Nota Prova 2:")
        entrada_trabalho = criar_entrada("Nota Trabalho:")

        resultado_label = tk.Label(media_win, text="", font=("Arial", 14), bg="#f5f5f5", fg="green")
        resultado_label.pack(pady=20)

        def calcular():
            try:
                p1 = float(entrada_prova1.get())
                p2 = float(entrada_prova2.get())
                trab = float(entrada_trabalho.get())
                if not all(0 <= nota <= 10 for nota in [p1, p2, trab]):
                    raise ValueError
                media = round(((p1 * 4) + (p2 * 4) + (trab * 2)) / 10, 2)
                if media >= 7:
                    resultado_label.config(text=f"Média Final: {media}\nParabéns, você foi aprovado!", fg="green")
                else:
                    resultado_label.config(text=f"Média Final: {media}\nVocê não atingiu a média para aprovação.", fg="red")
            except ValueError:
                resultado_label.config(text="Por favor, insira notas válidas (0 a 10).", fg="red")

        tk.Button(media_win, text="Calcular", font=("Arial", 12), bg="#4a7abc", fg="white", command=calcular).pack(pady=10)

    def sair():
        root.destroy()

    botoes_info = [
        ("📚 Documentos do Aluno", ver_documentos),
        ("📝 Trabalhos Acadêmicos", ver_desempenho),
        ("📆 Calendário", calendario),
        ("🎓 Aulas ao Vivo", aulas),
        ("📊 Calcular Média", calcular_media),
        ("🚪 Sair", sair)
    ]

    for i, (texto, comando) in enumerate(botoes_info):
        btn = tk.Button(btn_frame, text=texto, width=30, height=2, font=("Arial", 12, "bold"), bg="#4a7abc", fg="white", relief="raised", command=comando)
        btn.grid(row=i//2, column=i%2, padx=15, pady=15)

    root.mainloop()

# A função tela_cadastro e tela_login continua aqui, e o programa é iniciado com if __name__ == "__main__": tela_login()


def tela_cadastro():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Usuário")
    cadastro.geometry("500x600")
    cadastro.configure(bg="#f5f5f5")

    try:
        imagem_logo = Image.open(recurso_caminho("Imagens/23.png")).resize((120, 120), Image.Resampling.LANCZOS)
        imagem_logo = ImageTk.PhotoImage(imagem_logo)
        logo_label = tk.Label(cadastro, image=imagem_logo, bg="#f5f5f5")
        logo_label.image = imagem_logo
        logo_label.pack(pady=10)
    except Exception as e:
        print("Erro ao carregar imagem:", e)

    tk.Label(cadastro, text="Cadastro de Novo Usuário", font=("Arial", 18), bg="#f5f5f5").pack(pady=10)

    def criar_label_entry(texto):
        frame = tk.Frame(cadastro, bg="#f5f5f5")
        frame.pack(pady=5)
        label = tk.Label(frame, text=texto, width=15, anchor="w", bg="#f5f5f5")
        label.pack(side="left")
        entry = tk.Entry(frame, width=30)
        entry.pack(side="left")
        return entry

    nome_entry = criar_label_entry("Nome completo:")
    usuario_entry = criar_label_entry("Nome de usuário:")
    email_entry = criar_label_entry("E-mail:")
    senha_entry = criar_label_entry("Senha:")
    senha_entry.config(show="*")
    confirmar_entry = criar_label_entry("Confirmar senha:")
    confirmar_entry.config(show="*")

    def registrar():
        nome = nome_entry.get().strip()
        usuario = usuario_entry.get().strip()
        email = email_entry.get().strip()
        senha = senha_entry.get().strip()
        confirmar = confirmar_entry.get().strip()

        if not all([nome, usuario, email, senha, confirmar]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        sucesso, mensagem = salvar_usuario(nome, usuario, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            cadastro.destroy()
        else:
            messagebox.showerror("Erro", mensagem)

    tk.Button(cadastro, text="Cadastrar", font=("Arial", 12), bg="#4a7abc", fg="white", command=registrar).pack(pady=20)

def tela_login():
    login = tk.Tk()
    login.title("Sistema de Login")
    login.state('zoomed')

    largura = login.winfo_screenwidth()
    altura = login.winfo_screenheight()

    try:
        fundo_img = Image.open(recurso_caminho("Imagens/19.png")).resize((largura, altura), Image.Resampling.LANCZOS)
        fundo = ImageTk.PhotoImage(fundo_img)
    except Exception:
        fundo = None

    canvas = tk.Canvas(login, width=largura, height=altura, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    if fundo:
        canvas.create_image(0, 0, image=fundo, anchor="nw")

    if fundo:
        box_bg_img = Image.open(recurso_caminho("Imagens/19.png")).resize((400, 250), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(15))
        mask = Image.new("L", (400, 250), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, 400, 250), radius=30, fill=255)
        box_bg_img.putalpha(mask)
        box_bg = ImageTk.PhotoImage(box_bg_img)
        canvas.create_image(largura//2, altura//2, image=box_bg, anchor="center")

    canvas.create_text(largura//2, altura//2 - 80, text="Entre com o Login", font=("Arial Black", 28), fill="white")

    def clear_placeholder(event, entry, text):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="black", show="*" if entry == campo_senha else "")

    def add_placeholder(event, entry, text):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="gray", show="")

    campo_usuario = tk.Entry(login, font=("Arial", 14), width=25, fg="gray")
    campo_usuario.insert(0, "Usuário")
    campo_usuario.bind("<FocusIn>", lambda e: clear_placeholder(e, campo_usuario, "Usuário"))
    campo_usuario.bind("<FocusOut>", lambda e: add_placeholder(e, campo_usuario, "Usuário"))

    campo_senha = tk.Entry(login, font=("Arial", 14), width=25, fg="gray")
    campo_senha.insert(0, "Senha")
    campo_senha.bind("<FocusIn>", lambda e: clear_placeholder(e, campo_senha, "Senha"))
    campo_senha.bind("<FocusOut>", lambda e: add_placeholder(e, campo_senha, "Senha"))

    canvas.create_window(largura//2, altura//2 - 20, window=campo_usuario)
    canvas.create_window(largura//2, altura//2 + 30, window=campo_senha)

    def validar_login():
        usuario = campo_usuario.get()
        senha = campo_senha.get()
        if usuario == "Usuário" or senha == "Senha" or not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha os campos de usuário e senha.")
            return
        usuarios = carregar_usuarios()
        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                login.destroy()
                main_screen(u["nome"], u["cargo"], u["email"])
                return
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    # Botões
    espaco = 20
    largura_btn = 120
    pos_x_entrar = largura//2 - (largura_btn//2 + espaco//2)
    pos_x_cadastrar = largura//2 + (largura_btn//2 + espaco//2)
    pos_y = altura//2 + 80

    btn_entrar = tk.Button(login, text="Entrar", bg="#22a2f0", fg="white", font=("Arial", 14, "bold"), relief=tk.FLAT, width=10, command=validar_login)
    canvas.create_window(pos_x_entrar, pos_y, window=btn_entrar)

    btn_cadastro = tk.Button(login, text="Cadastrar", bg="#f05151", fg="white", font=("Arial", 14, "bold"), relief=tk.FLAT, width=10, command=tela_cadastro)
    canvas.create_window(pos_x_cadastrar, pos_y, window=btn_cadastro)

    login.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        # Modo compilação
        import subprocess

        sep = ";" if os.name == "nt" else ":"
        command = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            f"--add-data=Imagens{sep}Imagens",
            f"--add-data=usuarios.json{sep}.",
            "tela_login.py"
        ]

        print("Executando comando PyInstaller:")
        print(" ".join(command))
        subprocess.run(command)
    else:
        # Modo normal
        tela_login()