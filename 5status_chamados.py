import tkinter as tk
from tkinter import messagebox, scrolledtext
import psycopg2
from datetime import datetime

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

def atualizar_chamados():
    limpar_interactive_frame()
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT 
                    c.id, c.categoria_id, c.titulo, c.descricao, c.status, c.prioridade, c.data_abertura, c.data_fechamento,
                    u.nome, u.email, u.ip
                FROM 
                    chamados c
                JOIN 
                    usuarios u ON c.usuario_id = u.id
                WHERE 
                    c.status <> 'fechado'
                ORDER BY 
                    c.data_abertura
            """)
            rows = cur.fetchall()
            if not rows:
                tk.Label(interactive_frame, text="Nenhum chamado em aberto.").pack(anchor='w', padx=10, pady=5)
            for row in rows:
                info = (
                    f"ID do Chamado: {row[0]}, Categoria ID: {row[1]}\n"
                    f"Título: {row[2]}, Descrição: {row[3]}\n"
                    f"Status: {row[4]}, Prioridade: {row[5]}\n"
                    f"Data Abertura: {row[6]}, Data Fechamento: {row[7]}\n"
                    f"Usuário: {row[8]}, Email: {row[9]}, IP: {row[10]}"
                )
                frame = tk.Frame(interactive_frame, pady=5, padx=10)
                tk.Label(frame, text=info, justify=tk.LEFT, wraplength=700, anchor='w').pack(side=tk.LEFT, fill='x', expand=True)
                tk.Button(frame, text="Responder", command=lambda r=row: responder_chamado(r[0], r[9])).pack(side=tk.LEFT, padx=5)
                tk.Button(frame, text="Fechar", command=lambda r=row: fechar_chamado(r[0])).pack(side=tk.LEFT, padx=5)
                tk.Button(frame, text="Resposta do Cliente", command=lambda r=row: visualizar_respostas(r[0])).pack(side=tk.LEFT, padx=5)
                frame.pack(anchor='w', fill='x')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar chamados: {e}")
        finally:
            cur.close()
            conn.close()

def fechar_chamado(chamado_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            data_fechamento = datetime.now()
            cur.execute("UPDATE chamados SET status = 'fechado', data_fechamento = %s WHERE id = %s", (data_fechamento, chamado_id))
            conn.commit()
            messagebox.showinfo("Sucesso", "Chamado fechado com sucesso!")
            atualizar_chamados()  
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fechar chamado: {e}")
        finally:
            cur.close()
            conn.close()

def visualizar_respostas(chamado_id):
    resposta_janela = tk.Toplevel(root)
    resposta_janela.title("Respostas do Cliente")
    text_area = scrolledtext.ScrolledText(resposta_janela, height=10)
    text_area.pack()
    
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT mensagem FROM mensagens_chamados WHERE chamado_id = %s AND autor = 'cliente' ORDER BY data_envio", (chamado_id,))
            mensagens = cur.fetchall()
            for mensagem in mensagens:
                text_area.insert(tk.END, f"{mensagem[0]}\n\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar respostas: {e}")
        finally:
            cur.close()
            conn.close()

def responder_chamado(chamado_id, email_usuario):
    def enviar_resposta():
        resposta = resposta_text.get("1.0", tk.END).strip()
        if not resposta:
            messagebox.showwarning("Erro", "A resposta não pode estar vazia.")
            return
        conn = conectar_banco()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO mensagens_chamados (chamado_id, mensagem, autor) VALUES (%s, %s, 'admin')", (chamado_id, resposta))
                conn.commit()
                messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao enviar resposta: {e}")
            finally:
                cur.close()
                conn.close()
        resposta_janela.destroy()

    resposta_janela = tk.Toplevel(root)
    resposta_janela.title("Responder Chamado")
    tk.Label(resposta_janela, text="Digite sua resposta:").pack()
    resposta_text = scrolledtext.ScrolledText(resposta_janela, height=10)
    resposta_text.pack()
    tk.Button(resposta_janela, text="Enviar", command=enviar_resposta).pack(pady=10)

def carregar_mensagens(chamado_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT mensagem, autor FROM mensagens_chamados WHERE chamado_id = %s ORDER BY data_envio", (chamado_id,))
            mensagens = cur.fetchall()
            mensagens_text.config(state=tk.NORMAL)
            mensagens_text.delete("1.0", tk.END)
            for mensagem, autor in mensagens:
                prefixo = "Admin: " if autor == 'admin' else "Cliente: "
                mensagens_text.insert(tk.END, f"{prefixo}{mensagem}\n\n")
            mensagens_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar mensagens: {e}")
        finally:
            cur.close()
            conn.close()

def atualizar_mensagens(chamado_id):
    carregar_mensagens(chamado_id)
    root.after(5000, atualizar_mensagens, chamado_id)

#INTERFACE
root = tk.Tk()
root.title("Status dos Chamados")
root.geometry('800x600')

outer_frame = tk.Frame(root)
outer_frame.pack(expand=True, fill='both')

canvas = tk.Canvas(outer_frame)
scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

interactive_frame = scrollable_frame

tk.Button(root, text="Atualizar", command=atualizar_chamados).pack(pady=10)

atualizar_chamados()

root.mainloop()
