import tkinter as tk
from tkinter import messagebox
import psycopg2

def conectar_banco():
    try:
        return psycopg2.connect(
            dbname='',
            user='',  
            password='',  
            host=''
        )
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
        return None

def limpar_interactive_frame():
    for widget in interactive_frame.winfo_children():
        widget.destroy()

def criar_usuario():
    limpar_interactive_frame()
    tk.Label(interactive_frame, text="Nome do usuário:").pack()
    entry_nome_usuario = tk.Entry(interactive_frame)
    entry_nome_usuario.pack()

    tk.Label(interactive_frame, text="E-mail do usuário:").pack()
    entry_email_usuario = tk.Entry(interactive_frame)
    entry_email_usuario.pack()

    tk.Label(interactive_frame, text="IP do usuário:").pack()
    entry_ip_usuario = tk.Entry(interactive_frame)
    entry_ip_usuario.pack()

    tk.Label(interactive_frame, text="Senha do usuário:").pack()
    entry_senha_usuario = tk.Entry(interactive_frame, show="*")
    entry_senha_usuario.pack()
    
    tk.Label(interactive_frame, text="Tipo de usuário:").pack()
    role_var = tk.StringVar(value="user") 
    tk.Radiobutton(interactive_frame, text="Usuário", variable=role_var, value="user").pack(anchor=tk.W)
    tk.Radiobutton(interactive_frame, text="Administrador", variable=role_var, value="admin").pack(anchor=tk.W)

    #PASSAR ARGUMENTO 'ROLE' NA CHAMADA DA FUNÇÃO
    btn_salvar_usuario = tk.Button(interactive_frame, text="Salvar", command=lambda: salvar_usuario(
        entry_nome_usuario.get(), entry_email_usuario.get(), entry_senha_usuario.get(), role_var.get(), entry_ip_usuario.get()
    ))
    btn_salvar_usuario.pack()

def salvar_usuario(nome, email, senha, role, ip):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nome, email, senha, role, ip) VALUES (%s, %s, %s, %s, %s)", 
                        (nome, email, senha, role, ip))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Usuário {nome} criado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar usuário: {e}")
        finally:
            cur.close()
            conn.close()


def lista_usuarios():
    limpar_interactive_frame()
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, nome, email, senha, role, ip FROM usuarios")
            row = cur.fetchone()
            while row is not None:
                info = f"ID: {row[0]}, Nome: {row[1]}, Email: {row[2]}, Senha: {row[3]}, Role: {row[4]}, IP: {row[5]}"
                tk.Label(interactive_frame, text=info).pack()
                row = cur.fetchone()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar usuários: {e}")
        finally:
            cur.close()
            conn.close()

def listar_chamados():
    limpar_interactive_frame()
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT c.id, c.titulo, c.descricao, c.status, c.prioridade, c.data_abertura, u.nome FROM chamados c JOIN usuarios u ON c.usuario_id = u.id")
            rows = cur.fetchall()
            for row in rows:
                info = f"ID: {row[0]}, Título: {row[1]}, Descrição: {row[2]}, Status: {row[3]}, Prioridade: {row[4]}, Data: {row[5]}, Usuário: {row[6]}"
                tk.Label(interactive_frame, text=info).pack()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar chamados: {e}")
        finally:
            cur.close()
            conn.close()

def listar_categorias():
    limpar_interactive_frame()
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, nome, descricao FROM categorias_chamados")
            rows = cur.fetchall()
            for row in rows:
                info = f"ID: {row[0]}, Nome: {row[1]}, Descrição: {row[2]}"
                tk.Label(interactive_frame, text=info).pack()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar categorias: {e}")
        finally:
            cur.close()
            conn.close()

def adicionar_categoria():
    limpar_interactive_frame()
    tk.Label(interactive_frame, text="Nome da Categoria:").pack()
    entry_nome_categoria = tk.Entry(interactive_frame)
    entry_nome_categoria.pack()

    tk.Label(interactive_frame, text="Descrição:").pack()
    entry_descricao_categoria = tk.Entry(interactive_frame)
    entry_descricao_categoria.pack()

    btn_salvar_categoria = tk.Button(interactive_frame, text="Salvar", command=lambda: salvar_categoria(
        entry_nome_categoria.get(), entry_descricao_categoria.get()
    ))
    btn_salvar_categoria.pack()

def salvar_categoria(nome, descricao):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO categorias_chamados (nome, descricao) VALUES (%s, %s)", (nome, descricao))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Categoria {nome} criada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar categoria: {e}")
        finally:
            cur.close()
            conn.close()

def listar_assuntos():
    limpar_interactive_frame()
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT a.id, c.nome, a.nome, a.prioridade, a.descricao FROM assuntos_chamados a JOIN categorias_chamados c ON a.categoria_id = c.id")
            rows = cur.fetchall()
            for row in rows:
                info = f"ID: {row[0]}, Categoria: {row[1]}, Assunto: {row[2]}, Prioridade: {row[3]}, Descrição: {row[4]}"
                tk.Label(interactive_frame, text=info).pack()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar assuntos: {e}")
        finally:
            cur.close()
            conn.close()

def adicionar_assunto():
    limpar_interactive_frame()
    conn = conectar_banco()
    categorias = []
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, nome FROM categorias_chamados")
            categorias = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar categorias: {e}")
        finally:
            cur.close()

    tk.Label(interactive_frame, text="Categoria:").pack()
    categoria_var = tk.StringVar()
    categoria_menu = tk.OptionMenu(interactive_frame, categoria_var, *[cat[1] for cat in categorias])
    categoria_menu.pack()

    tk.Label(interactive_frame, text="Nome do Assunto:").pack()
    entry_nome_assunto = tk.Entry(interactive_frame)
    entry_nome_assunto.pack()

    tk.Label(interactive_frame, text="Prioridade:").pack()
    entry_prioridade_assunto = tk.Entry(interactive_frame)
    entry_prioridade_assunto.pack()

    tk.Label(interactive_frame, text="Descrição:").pack()
    entry_descricao_assunto = tk.Entry(interactive_frame)
    entry_descricao_assunto.pack()

    btn_salvar_assunto = tk.Button(interactive_frame, text="Salvar", command=lambda: salvar_assunto(
        categoria_var.get(), entry_nome_assunto.get(), entry_prioridade_assunto.get(), entry_descricao_assunto.get()
    ))
    btn_salvar_assunto.pack()

def salvar_assunto(categoria, nome, prioridade, descricao):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM categorias_chamados WHERE nome = %s", (categoria,))
            categoria_id = cur.fetchone()[0]
            cur.execute("INSERT INTO assuntos_chamados (categoria_id, nome, prioridade, descricao) VALUES (%s, %s, %s, %s)", (categoria_id, nome, prioridade, descricao))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Assunto {nome} criado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar assunto: {e}")
        finally:
            cur.close()
            conn.close()

#INTERFACE
root = tk.Tk()
root.title("Tela de Configurações - Admin-only")
root.geometry('800x600')
sidebar = tk.Frame(root, width=200, bg='#CCC', height=600, relief='sunken', borderwidth=2)
sidebar.pack(expand=False, fill='y', side='left', anchor='nw')
main_content = tk.Frame(root, bg='#FFF', width=600, height=600)
main_content.pack(expand=True, fill='both', side='right')
interactive_frame = tk.Frame(main_content, bg='#FFF')
interactive_frame.pack(expand=True, fill='both')

dark_bg = "#243837"
light_bg = "#3e3e3e"
text_color = "#FE7833"
highlight_color = "#463746"
#ADICIONAR BOTÕES AQUI
buttons = {
    "Criar Usuário + Senha": criar_usuario,
    "Lista de Usuários": lista_usuarios,
    "Listar Chamados": listar_chamados,
}

for text, command in buttons.items():
    tk.Button(sidebar, text=text, command=command).pack(fill='x')

root.mainloop()





