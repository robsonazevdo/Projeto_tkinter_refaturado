import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror, askquestion
from datetime import datetime, date
import shutil
import os

class Backup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Backup de Dados")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        self.configure(bg="#b4918f")
        frame = tk.Frame(self, bg="#b4918f")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Entrada de origem (preenchida com 'agenda.db')
        label_origem = tk.Label(frame, text="Arquivo de Origem:", bg="#b4918f")
        label_origem.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        entrada_origem = tk.Entry(frame, width=50, bg="#b4918f")
        entrada_origem.grid(row=0, column=1, padx=10, pady=10)
        entrada_origem.insert(0, "agenda.db")
        entrada_origem.config(state='readonly')

        # Entrada de destino
        label_destino = tk.Label(frame, text="Diretório de Destino:", bg="#b4918f")
        label_destino.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entrada_destino = tk.Entry(frame, width=50, bg="#b4918f")
        self.entrada_destino.grid(row=1, column=1, padx=10, pady=10)

        botao_destino = tk.Button(frame, text="Selecionar", font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5,command=self.selecionar_destino)
        botao_destino.grid(row=1, column=2, padx=10, pady=10)

        # Botão para fazer backup
        botao_backup = tk.Button(frame, text="Fazer Backup", font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5, command=self.fazer_backup)
        botao_backup.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Botão para carregar backup
        botao_carregar = tk.Button(frame, text="Carregar Backup", font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5, command=self.carregar_backup)
        botao_carregar.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

        self.focus_force()
        self.grab_set()



    def fazer_backup(self):
        try:
            origem = 'agenda.db'
            destino = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite database files", "*.db")])
            if destino:
                shutil.copy2(origem, destino)
                showinfo("Sucesso", "Backup realizado com sucesso!",psrent=self)
        except Exception as e:
            showerror("Erro", f"Erro ao realizar backup: {e}",psrent=self)
            

    def carregar_backup(self):
        destino = self.entrada_destino.get()
        origem_backup = filedialog.askopenfilename(
            title="Selecione o arquivo de backup",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")], parent=self
        )

        if not origem_backup:
            dados.fechar_conexoes()

        try:
            shutil.copy2(origem_backup, "agenda.db")
            showinfo("Restaurar Backup", "Backup restaurado com sucesso!",parent=self)
            self.destroy()
        except Exception as e:
            showerror("Erro", f"Erro ao restaurar backup: {e}", parent=self)


    def selecionar_destino(self):
        destino = filedialog.askdirectory(title="Selecione o diretório de destino", parent=self)
        if destino:
            self.entrada_destino.delete(0, tk.END)
            self.entrada_destino.insert(0, destino)

    