import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import psycopg2
from datetime import datetime
import json

# Adicione seu token e ID de chat do Telegram
telegram_token = "yourtelegramtoken"
telegram_chat_id = "yourtelegramchatid"

# Carregar o usuário logado de um arquivo JSON
with open('usuario_logado.json', 'r') as f:
    usuario_logado = json.load(f)

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

def obter_nome_usuario(usuario_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT nome FROM usuarios WHERE id = %s", (usuario_id,))
            usuario_nome = cur.fetchone()
            return usuario_nome[0] if usuario_nome else "Usuário desconhecido"
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter nome do usuário: {e}")
            return "Usuário desconhecido"
        finally:
            cur.close()
            conn.close()

def obter_tipos_chamado():
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, nome FROM categorias_chamados")
            return {row[1]: row[0] for row in cur.fetchall()}
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter tipos de chamado: {e}")
            return {}
        finally:
            cur.close()
            conn.close()

def obter_assuntos(tipo_chamado_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT a.nome 
                FROM assuntos_chamados a 
                JOIN categorias_chamados c ON a.categoria_id = c.id 
                WHERE c.id = %s
            """, (tipo_chamado_id,))
            return [row[0] for row in cur.fetchall()]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter assuntos: {e}")
            return []
        finally:
            cur.close()
            conn.close()

def obter_localidades():
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, nome FROM localidades")
            return {row[1]: row[0] for row in cur.fetchall()}
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter localidades: {e}")
            return {}
        finally:
            cur.close()
            conn.close()

def atualizar_assuntos(*args):
    tipo_chamado = tipo_chamado_var.get()
    tipo_chamado_id = tipos_chamado[tipo_chamado]
    assuntos = obter_assuntos(tipo_chamado_id)
    assunto_var.set('')
    menu = assunto_option_menu['menu']
    menu.delete(0, 'end')
    for assunto in assuntos:
        menu.add_command(label=assunto, command=tk._setit(assunto_var, assunto))

def enviar_chamado():
    tipo_chamado = tipo_chamado_var.get()
    tipo_chamado_id = tipos_chamado.get(tipo_chamado)
    assunto = assunto_var.get()
    descricao = descricao_text.get("1.0", tk.END).strip()
    localidade = localidade_var.get()
    localidade_id = localidades.get(localidade)

    if not tipo_chamado_id or not assunto or not descricao or not localidade_id:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
        return

    conn = conectar_banco()
    prioridade = None
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT a.prioridade FROM assuntos_chamados a WHERE a.nome = %s AND a.categoria_id = %s", (assunto, tipo_chamado_id))
            prioridade = cur.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao determinar prioridade: {e}")
        finally:
            cur.close()

    if prioridade is None:
        messagebox.showwarning("Erro", "Não foi possível determinar a prioridade.")
        return

    usuario_id = usuario_logado['id']
    usuario_nome = obter_nome_usuario(usuario_id)
    message = f"Novo chamado recebido!\nUsuário: {usuario_nome}\nTipo: {tipo_chamado}\nAssunto: {assunto}\nDescrição: {descricao}\nPrioridade: {prioridade}\nLocalidade: {localidade}"

    # NOTIFICAÇÃO TELEGRAM
    try:
        response = requests.get(
            f"https://api.telegram.org/botcodigodobot:codigotoken/sendMessage",
            params={"chat_id": telegram_chat_id, "text": message}
        )
        if response.status_code != 200:
            messagebox.showwarning("Erro", "Não foi possível enviar a notificação no Telegram.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar notificação: {str(e)}")

    # Registrar chamado no banco de dados
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO chamados (usuario_id, categoria_id, titulo, descricao, status, prioridade, data_abertura, localidade_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (usuario_id, tipo_chamado_id, assunto, descricao, 'aberto', prioridade, datetime.now(), localidade_id)
            )
            chamado_id = cur.fetchone()[0]
            conn.commit()
            messagebox.showinfo("Chamado", f"Chamado enviado e registrado com sucesso! ID do Chamado: {chamado_id}")
            enviar_button.config(state=tk.DISABLED)
            carregar_detalhes_chamado(chamado_id)
            verificar_respostas(chamado_id)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar chamado: {e}")
        finally:
            cur.close()
            conn.close()

def carregar_detalhes_chamado(chamado_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, categoria_id, titulo, descricao, status, prioridade, data_abertura FROM chamados WHERE id = %s", (chamado_id,))
            chamado = cur.fetchone()
            if chamado:
                detalhes = (
                    f"ID do Chamado: {chamado[0]}\n"
                    f"Categoria ID: {chamado[1]}\n"
                    f"Título: {chamado[2]}\n"
                    f"Descrição: {chamado[3]}\n"
                    f"Status: {chamado[4]}\n"
                    f"Prioridade: {chamado[5]}\n"
                    f"Data Abertura: {chamado[6]}"
                )
                detalhes_label.config(text=detalhes)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar detalhes do chamado: {e}")
        finally:
            cur.close()
            conn.close()

def verificar_respostas(chamado_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT mensagem FROM mensagens_chamados WHERE chamado_id = %s AND autor = 'admin' ORDER BY data_envio DESC LIMIT 1", (chamado_id,))
            resposta = cur.fetchone()
            if resposta:
                messagebox.showinfo("Resposta do Administrador", resposta[0])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar respostas: {e}")
        finally:
            cur.close()
            conn.close()
    root.after(5000, verificar_respostas, chamado_id)

def limpar_campos():
    tipo_chamado_var.set('')
    assunto_var.set('')
    descricao_text.delete("1.0", tk.END)
    localidade_var.set('')
    enviar_button.config(state=tk.NORMAL)

#INTERFACE
dark_bg = "#243837"
light_bg = "#3e3e3e"
text_color = "#FE7833"
highlight_color = "#463746"

root = tk.Tk()
root.title("TEC HELP: Abertura de Chamados")
root.geometry('700x700')
root.configure(bg=dark_bg)

tk.Label(root, text="Tipo de chamado:", bg=dark_bg, fg=text_color).pack(pady=5)
tipos_chamado = obter_tipos_chamado()
tipo_chamado_var = tk.StringVar(root)
tipo_chamado_var.trace('w', atualizar_assuntos)
tipo_chamado_option_menu = tk.OptionMenu(root, tipo_chamado_var, *tipos_chamado.keys())
tipo_chamado_option_menu.configure(bg=light_bg, fg=text_color)
tipo_chamado_option_menu.pack()

tk.Label(root, text="Assunto:", bg=dark_bg, fg=text_color).pack(pady=5)
assunto_var = tk.StringVar(root)
assunto_option_menu = tk.OptionMenu(root, assunto_var, '')
assunto_option_menu.configure(bg=light_bg, fg=text_color)
assunto_option_menu.pack()

tk.Label(root, text="Localidade:", bg=dark_bg, fg=text_color).pack(pady=5)
localidades = obter_localidades()
localidade_var = tk.StringVar(root)
localidade_option_menu = tk.OptionMenu(root, localidade_var, *localidades.keys())
localidade_option_menu.configure(bg=light_bg, fg=text_color)
localidade_option_menu.pack()

tk.Label(root, text="Descrição do Chamado:", bg=dark_bg, fg=text_color).pack(pady=5)
descricao_text = scrolledtext.ScrolledText(root, height=10, bg=light_bg, fg=text_color, insertbackground=text_color)
descricao_text.pack()

enviar_button = tk.Button(root, text="Enviar", command=enviar_chamado, bg=highlight_color, fg=text_color)
enviar_button.pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(root, text="Cancelar", command=limpar_campos, bg=highlight_color, fg=text_color).pack(side=tk.RIGHT, padx=10, pady=10)

detalhes_label = tk.Label(root, text="", justify=tk.LEFT, bg=dark_bg, fg=text_color)
detalhes_label.pack()

root.mainloop()



