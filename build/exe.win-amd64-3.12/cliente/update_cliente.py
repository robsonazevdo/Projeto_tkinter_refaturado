import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno

# from maskedentry import*
from tkcalendar import DateEntry
from operator import neg
# import calendario


class Update_Cliente(tk.Toplevel):
    def __init__(self, parent, edicao_position):
        super().__init__(parent)

        self.id = edicao_position[0]
        self.nome = edicao_position[1]
        self.tel = edicao_position[2]

        self.title("Atualizar Cliente")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = self.winfo_screenwidth() // 4
        y = int(self.winfo_screenheight() * 0.2)
        self.geometry('700x500+' + str(x) + '+' + str(y))
        self.configure(background="#b4918f")

        tk.Label(
            self,
            text="Id Cliente",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 12),
            bd=5
        ).pack(pady=(20, 0))

        self.codigo_cliente = tk.Entry(self, width=65, font=('TkMenuFont', 10))
        self.codigo_cliente.pack(pady=(20, 0))
        self.codigo_cliente.insert(0, self.id)  # Define o valor inicial para self.id
        self.codigo_cliente.config(state='readonly')  # Torna o campo somente leitura

        tk.Label(
            self,
            text="Nome cliente",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 12),
            bd=5
        ).pack(pady=(20, 0))

        self.nome_cliente = tk.Entry(self, width=65, font=('TkMenuFont', 10))
        self.nome_cliente.pack(pady=(20, 0))
        self.nome_cliente.insert(0, self.nome)  # Define o valor inicial para self.nome

        tk.Label(
            self,
            text="Telefone",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 12),
        ).pack(pady=(40, 0))

        self.Telefone = tk.Entry(self, width=65, font=('TkMenuFont', 10))
        self.Telefone.pack(pady=(20, 0))
        self.Telefone.insert(0, self.tel)  # Define o valor inicial para self.tel

        # Frame para os botões
        button_frame = tk.Frame(self, bg="#b4918f")
        button_frame.pack(pady=(8, 0))

        tk.Button(
            button_frame,
            text=("Atualizar"),
            font=('TkMenuFont', 15),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5,
            command=lambda: self.editar_cliente()
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text=("Deletar"),
            font=('TkMenuFont', 15),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5,
            command=lambda: self.deletar_cliente()
        ).pack(side=tk.LEFT, padx=10)

        self.transient()
        self.focus_force()
        self.grab_set()


    def editar_cliente(self):
        if self.codigo_cliente.get() == "" or self.nome_cliente.get() == "" or self.Telefone.get() == "":
            return showinfo(title=False, message="Preencha todos os campos", parent=self)

        confirm = askyesno(title="Confirmar", message="Você tem certeza que deseja atualizar o cliente?", parent=self)

        if confirm:
            dados.db_editar_cliente(self.codigo_cliente.get(), self.nome_cliente.get(), self.Telefone.get())
            showinfo(title=False, message="Cadastro atualizado com sucesso", parent=self)
            self.destroy()
            self.chamar_tela_anterior()

    def deletar_cliente(self):
        confirm = askyesno(title="Confirmar", message="Você tem certeza que deseja deletar o cliente?", parent=self)

        if confirm:
            dados.apagar_cliente(self.codigo_cliente.get(), self.nome_cliente.get())
            showinfo(title=False, message="Cliente deletado com sucesso", parent=self)
            self.destroy()
            self.chamar_tela_anterior()


    def chamar_tela_anterior(self):
        from cliente.pequisar_cliente import Pesquisar_Cliente
        Pesquisar_Cliente(self.master)