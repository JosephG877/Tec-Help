import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
import psycopg2
import json
from PIL import Image, ImageTk

# Variável global para armazenar o usuário logado
usuario_logado = {}

def conectar_banco():
    try:
        return psycopg2.connect(
            dbname='tgbrsuporte',
            user='master',
            password='!@#master2024',
            host='192.168.50.27'
        )
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
        return None

def validar_login(nome_usuario, senha):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, role FROM usuarios WHERE nome = %s AND senha = %s", (nome_usuario, senha))
            user = cur.fetchone()
            if user:
                global usuario_logado
                usuario_logado = {"id": user[0], "role": user[1]}
                # Salvar o usuário logado em um arquivo JSON
                with open(resource_path('usuario_logado.json'), 'w') as f:
                    json.dump(usuario_logado, f)
                messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {nome_usuario}!")
                if user[1] == "admin":
                    abrir_tela_admin()
                else:
                    abrir_tela_usuario()
            else:
                messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao validar login: {e}")
        finally:
            cur.close()
            conn.close()

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for network """
    base_path = os.path.abspath(os.path.dirname(__file__))
    abs_path = os.path.join(base_path, relative_path)
    print(f"Resolvendo caminho para {relative_path}: {abs_path}")
    return abs_path

def abrir_tela_admin():
    subprocess.Popen([sys.executable, resource_path('3tela_admin.py')])
    root.quit()

def abrir_tela_usuario():
    subprocess.Popen([sys.executable, resource_path('2ab_chamados.py')])
    root.quit()

# Interface de login
root = tk.Tk()
root.title("TEC HELP :: LOGIN")
root.geometry('800x600')

# Definir estilo de tema escuro
dark_bg = "#243837"
light_bg = "#3e3e3e"
text_color = "#FE7833"
highlight_color = "#463746"

root.configure(bg=dark_bg)

# Adicionar espaço para logo
logo_frame = tk.Frame(root, bg=dark_bg, height=150)
logo_frame.pack(fill=tk.X)

# Carregar a imagem da logo
try:
    logo_path = resource_path("techelplogo.jpg")
    print(f"Logo path: {logo_path}")  # Depurar caminho da logo
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((400, 200), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(logo_frame, image=logo_photo, bg=dark_bg)
    logo_label.image = logo_photo  # Manter uma referência para evitar que a imagem seja coletada pelo garbage collector
    logo_label.pack(pady=10)
except Exception as e:
    messagebox.showerror("Erro", f"Erro ao carregar a imagem da logo: {e}")

# Espaço para os campos de login
login_frame = tk.Frame(root, bg=dark_bg)
login_frame.pack(expand=True)

tk.Label(login_frame, text="Nome de Usuário:", bg=dark_bg, fg=text_color, font=('Arial', 22)).pack(pady=10)
entry_nome_usuario = tk.Entry(login_frame, bg=light_bg, fg=text_color, insertbackground=text_color, font=('Arial', 22), width=25)
entry_nome_usuario.pack(pady=5)

tk.Label(login_frame, text="Senha:", bg=dark_bg, fg=text_color, font=('Arial', 22)).pack(pady=10)
entry_senha = tk.Entry(login_frame, show="*", bg=light_bg, fg=text_color, insertbackground=text_color, font=('Arial', 22), width=25)
entry_senha.pack(pady=5)

tk.Button(login_frame, text="LOGIN", command=lambda: validar_login(entry_nome_usuario.get(), entry_senha.get()), bg=highlight_color, fg=text_color, font=('Arial', 14), width=20).pack(pady=20)

root.mainloop()
