import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import subprocess
import psycopg2
from tkinter import ttk
from datetime import datetime
import pandas as pd

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

def abrir_tela_configuracoes():
    subprocess.run(["python", "4tela_config_main.py"])

def abrir_tela_status_chamados():
    subprocess.run(["python", "5status_chamados.py"])

# Funções para gerenciar tipos de chamado
def listar_tipos_chamado():
    limpar_interactive_frame()
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, nome, descricao FROM categorias_chamados")
            rows = cur.fetchall()
            for row in rows:
                info = f"ID: {row[0]}, Nome: {row[1]}, Descrição: {row[2]}"
                frame = tk.Frame(interactive_frame)
                tk.Label(frame, text=info).pack(side=tk.LEFT)
                tk.Button(frame, text="Editar", command=lambda r=row: editar_tipo_chamado(r[0])).pack(side=tk.LEFT)
                tk.Button(frame, text="Deletar", command=lambda r=row: deletar_tipo_chamado(r[0])).pack(side=tk.LEFT)
                frame.pack()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar tipos de chamado: {e}")
        finally:
            cur.close()
            conn.close()

def adicionar_tipo_chamado():
    limpar_interactive_frame()
    tk.Label(interactive_frame, text="Nome do Tipo de Chamado:").pack()
    entry_nome_tipo_chamado = tk.Entry(interactive_frame)
    entry_nome_tipo_chamado.pack()

    tk.Label(interactive_frame, text="Descrição:").pack()
    entry_descricao_tipo_chamado = tk.Entry(interactive_frame)
    entry_descricao_tipo_chamado.pack()

    btn_salvar_tipo_chamado = tk.Button(interactive_frame, text="Salvar", command=lambda: salvar_tipo_chamado(
        entry_nome_tipo_chamado.get(), entry_descricao_tipo_chamado.get()
    ))
    btn_salvar_tipo_chamado.pack()

def salvar_tipo_chamado(nome, descricao, tipo_chamado_id=None):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            if tipo_chamado_id:
                cur.execute("UPDATE categorias_chamados SET nome = %s, descricao = %s WHERE id = %s", (nome, descricao, tipo_chamado_id))
                msg = f"Tipo de chamado {nome} atualizado com sucesso!"
            else:
                cur.execute("INSERT INTO categorias_chamados (nome, descricao) VALUES (%s, %s)", (nome, descricao))
                msg = f"Tipo de chamado {nome} criado com sucesso!"
            conn.commit()
            messagebox.showinfo("Sucesso", msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar tipo de chamado: {e}")
        finally:
            cur.close()
            conn.close()

def deletar_tipo_chamado(tipo_chamado_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM categorias_chamados WHERE id = %s", (tipo_chamado_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Tipo de chamado deletado com sucesso!")
            listar_tipos_chamado()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar tipo de chamado: {e}")
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
                info = f"ID: {row[0]}, Tipo de Chamado: {row[1]}, Assunto: {row[2]}, Prioridade: {row[3]}, Descrição: {row[4]}"
                frame = tk.Frame(interactive_frame)
                tk.Label(frame, text=info).pack(side=tk.LEFT)
                tk.Button(frame, text="Editar", command=lambda r=row: editar_assunto(r[0])).pack(side=tk.LEFT)
                tk.Button(frame, text="Deletar", command=lambda r=row: deletar_assunto(r[0])).pack(side=tk.LEFT)
                frame.pack()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar assuntos: {e}")
        finally:
            cur.close()
            conn.close()

def adicionar_assunto():
    limpar_interactive_frame()
    conn = conectar_banco()
    tipos_chamado = []
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, nome FROM categorias_chamados")
            tipos_chamado = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar tipos de chamado: {e}")
        finally:
            cur.close()

    tk.Label(interactive_frame, text="Tipo de Chamado:").pack()
    tipo_chamado_var = tk.StringVar()
    tipo_chamado_menu = tk.OptionMenu(interactive_frame, tipo_chamado_var, *[tipo[1] for tipo in tipos_chamado])
    tipo_chamado_menu.pack()

    tk.Label(interactive_frame, text="Nome do Assunto:").pack()
    entry_nome_assunto = tk.Entry(interactive_frame)
    entry_nome_assunto.pack()

    tk.Label(interactive_frame, text="Prioridade (1 a 5):").pack()
    entry_prioridade_assunto = tk.Entry(interactive_frame)
    entry_prioridade_assunto.pack()

    tk.Label(interactive_frame, text="Descrição:").pack()
    entry_descricao_assunto = tk.Entry(interactive_frame)
    entry_descricao_assunto.pack()

    btn_salvar_assunto = tk.Button(interactive_frame, text="Salvar", command=lambda: salvar_assunto(
        tipo_chamado_var.get(), entry_nome_assunto.get(), entry_prioridade_assunto.get(), entry_descricao_assunto.get()
    ))
    btn_salvar_assunto.pack()

def salvar_assunto(tipo_chamado_nome, nome, prioridade, descricao, assunto_id=None):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM categorias_chamados WHERE nome = %s", (tipo_chamado_nome,))
            tipo_chamado_id = cur.fetchone()[0]
            if assunto_id:
                cur.execute("UPDATE assuntos_chamados SET categoria_id = %s, nome = %s, prioridade = %s, descricao = %s WHERE id = %s", 
                            (tipo_chamado_id, nome, prioridade, descricao, assunto_id))
                msg = f"Assunto {nome} atualizado com sucesso!"
            else:
                cur.execute("INSERT INTO assuntos_chamados (categoria_id, nome, prioridade, descricao) VALUES (%s, %s, %s, %s)", 
                            (tipo_chamado_id, nome, prioridade, descricao))
                msg = f"Assunto {nome} criado com sucesso!"
            conn.commit()
            messagebox.showinfo("Sucesso", msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar assunto: {e}")
        finally:
            cur.close()
            conn.close()

def deletar_assunto(assunto_id):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM assuntos_chamados WHERE id = %s", (assunto_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Assunto deletado com sucesso!")
            listar_assuntos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar assunto: {e}")
        finally:
            cur.close()
            conn.close()

def gerar_relatorio():
    limpar_interactive_frame()

    #FILTROS DE DATA
    tk.Label(interactive_frame, text="Data Inicial (DD/MM/AAAA):").pack(pady=5)
    entry_data_inicial = tk.Entry(interactive_frame)
    entry_data_inicial.pack()

    tk.Label(interactive_frame, text="Data Final (DD/MM/AAAA):").pack(pady=5)
    entry_data_final = tk.Entry(interactive_frame)
    entry_data_final.pack()

    tk.Label(interactive_frame, text="Status:").pack(pady=5)
    status_var = tk.StringVar()
    status_var.set("Todos")
    status_menu = tk.OptionMenu(interactive_frame, status_var, "Todos", "Aberto", "Fechado")
    status_menu.pack()

    tk.Label(interactive_frame, text="Usuário:").pack(pady=5)
    entry_usuario = tk.Entry(interactive_frame)
    entry_usuario.pack()

    btn_gerar = tk.Button(interactive_frame, text="GERAR RELATÓRIO", command=lambda: exibir_relatorio(
        entry_data_inicial.get(),
        entry_data_final.get(),
        status_var.get(),
        entry_usuario.get()
    ))
    btn_gerar.pack(pady=20)

def exibir_relatorio(data_inicial, data_final, status, usuario):
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        try:
            data_inicial_formatada = None
            data_final_formatada = None

            if data_inicial:
                try:
                    data_inicial_formatada = datetime.strptime(data_inicial, "%d/%m/%Y").strftime("%Y-%m-%d 00:00:00")
                except ValueError:
                    messagebox.showerror("Erro", "Data inicial inválida. Use o formato DD/MM/AAAA.")
                    return

            if data_final:
                try:
                    data_final_formatada = datetime.strptime(data_final, "%d/%m/%Y").strftime("%Y-%m-%d 23:59:59")
                except ValueError:
                    messagebox.showerror("Erro", "Data final inválida. Use o formato DD/MM/AAAA.")
                    return

            query = """
                SELECT c.id, c.titulo, c.descricao, c.status, c.prioridade, c.data_abertura, c.data_fechamento,
                       u.nome AS usuario
                FROM chamados c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE (%s IS NULL OR c.data_abertura >= %s)
                  AND (%s IS NULL OR c.data_abertura <= %s)
                  AND (%s IS NULL OR c.status = %s)
                  AND (%s IS NULL OR u.nome ILIKE %s)
            """
            params = [
                data_inicial_formatada, data_inicial_formatada,
                data_final_formatada, data_final_formatada,
                status if status != "Todos" else None, status if status != "Todos" else None,
                usuario if usuario else None, f"%{usuario}%" if usuario else None
            ]
            cur.execute(query, params)
            rows = cur.fetchall()

            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Título", "Descrição", "Status", "Prioridade", "Data Abertura", "Data Fechamento", "Usuário"])

                text_area = scrolledtext.ScrolledText(interactive_frame, wrap=tk.WORD, width=100, height=20)
                text_area.pack()
                for row in rows:
                    text_area.insert(tk.END, f"ID: {row[0]}, Título: {row[1]}, Descrição: {row[2]}, Status: {row[3]}, "
                                             f"Prioridade: {row[4]}, Data Abertura: {row[5]}, Data Fechamento: {row[6]}, "
                                             f"Usuário: {row[7]}\n")

                btn_export_csv = tk.Button(interactive_frame, text="Exportar CSV", command=lambda: exportar_csv(df))
                btn_export_csv.pack()
                
            else:
                messagebox.showinfo("Relatório", "Nenhum chamado encontrado com os filtros selecionados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
        finally:
            cur.close()
            conn.close()

def exportar_csv(df):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso para {file_path}.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar relatório: {e}")


#INTERFACE 
root = tk.Tk()
root.title("Sistema de Suporte")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

interactive_frame = tk.Frame(main_frame)
interactive_frame.pack(fill=tk.BOTH, expand=True)

btn_configuracoes = tk.Button(main_frame, text="Configurações", command=abrir_tela_configuracoes)
btn_configuracoes.pack(side=tk.LEFT)

btn_status_chamados = tk.Button(main_frame, text="Status dos Chamados", command=abrir_tela_status_chamados)
btn_status_chamados.pack(side=tk.LEFT)

btn_listar_tipos_chamado = tk.Button(main_frame, text="Tipos de Chamado", command=listar_tipos_chamado)
btn_listar_tipos_chamado.pack(side=tk.LEFT)

btn_adicionar_tipo_chamado = tk.Button(main_frame, text="Adicionar Tipo de Chamado", command=adicionar_tipo_chamado)
btn_adicionar_tipo_chamado.pack(side=tk.LEFT)

btn_listar_assuntos = tk.Button(main_frame, text="Assuntos", command=listar_assuntos)
btn_listar_assuntos.pack(side=tk.LEFT)

btn_adicionar_assunto = tk.Button(main_frame, text="Adicionar Assunto", command=adicionar_assunto)
btn_adicionar_assunto.pack(side=tk.LEFT)

btn_gerar_relatorio = tk.Button(main_frame, text="GERAR RELATÓRIO", command=gerar_relatorio)
btn_gerar_relatorio.pack(side=tk.LEFT)

root.mainloop()

