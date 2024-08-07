import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkcalendar import DateEntry

class Servico(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Cadastrar Serviço")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = self.winfo_screenwidth() // 10
        y = int(self.winfo_screenheight() * 0.03)
        self.geometry('1000x690+' + str(x) + '+' + str(y))
        self.configure(background="#b4918f")

        self.create_treeview()
        self.create_widgets()
        self.buscar_servico()
        self.load_services()
        
        self.transient()
        self.focus_force()
        self.grab_set()

    def create_widgets(self):
        self.frame_cadastro = tk.LabelFrame(self, text="Cadastrar Serviço", bg="#b4918f", fg="white", font=('TkMenuFont', 12))
        self.frame_cadastro.pack(padx=10, pady=10, fill="both", expand=True)

        # Create a frame to hold the form
        form_frame = tk.Frame(self.frame_cadastro, bg="#b4918f")
        form_frame.pack(pady=20, padx=20)

        # Nome do Serviço
        tk.Label(form_frame, text="Nome do Serviço", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=0, column=0, pady=5, sticky='e')
        self.nome_servico = tk.Entry(form_frame, width=65, font=('TkMenuFont', 10))
        self.nome_servico.grid(row=0, column=1, pady=5, padx=10)

        # Preço Serviço
        tk.Label(form_frame, text="Preço Serviço", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=1, column=0, pady=5, sticky='e')
        self.preco_servico = tk.Entry(form_frame, width=65, font=('TkMenuFont', 10))
        self.preco_servico.grid(row=1, column=1, pady=5, padx=10)

        # Duração Serviço
        tk.Label(form_frame, text="Duração Serviço", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=2, column=0, pady=5, sticky='e')
        self.duracao_servico = tk.Entry(form_frame, width=65, font=('TkMenuFont', 10))
        self.duracao_servico.grid(row=2, column=1, pady=5, padx=10)

        # Checkbox
        tk.Label(form_frame, text="Status", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=3, column=0, pady=5, sticky='e')
        self.var = tk.IntVar()
        checkbox = tk.Checkbutton(form_frame, text="Ativo", variable=self.var, onvalue=1, offvalue=2, bg="#b4918f")
        checkbox.grid(row=3, column=1, pady=5, sticky='w')

        # Cargo Combobox
        tk.Label(form_frame, text="Quem Realiza?", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=3, column=1, pady=5, sticky='e')
        cargo = dados.db_listar_cargo()
        self.cargo_map = {c['nome_cargo']: c['id_cargo'] for c in cargo}
        cargo_names = list(self.cargo_map.keys())
        self.cargo_map_inverse = {v: k for k, v in self.cargo_map.items()}
        self.textArea = ttk.Combobox(form_frame, values=cargo_names)
        self.textArea.grid(row=3, column=2, pady=5, padx=10, sticky='w')

        # Cadastrar Button
        tk.Button(form_frame, text="Cadastrar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.criar_servico).grid(row=5, column=1, pady=20, sticky='w')

    def criar_servico(self):
        estado = "ativo" if self.var.get() == 1 else "inativo"
        
        if self.nome_servico.get() == "" or self.preco_servico.get() == "" or self.duracao_servico.get() == "" or self.textArea.get() == "":
            return showinfo(title=False, message="Preencha todos os campos", parent=self)
        
        selected_cargo = self.textArea.get()
        if selected_cargo in self.cargo_map:
            selected_id_cargo = self.cargo_map[selected_cargo]
            
        ja_existe, s = dados.criar_servico(self.nome_servico.get().strip(" ").capitalize(), self.preco_servico.get(), self.duracao_servico.get(), estado, selected_id_cargo)
        if ja_existe != False:
            self.nome_servico.delete(0, tk.END)
            self.preco_servico.delete(0, tk.END)
            self.duracao_servico.delete(0, tk.END)
            return showinfo(title=False, message="Serviço Já existe", parent=self)
            
        else:
            showinfo(title=False, message="Cadastro feito com sucesso", parent=self)
            self.tree.insert("", "end", values=(s["id_servico"], s["nome_servico"], s["preco_servico"], s["duracao_servico"], estado.capitalize()))
            self.nome_servico.delete(0, tk.END)
            self.preco_servico.delete(0, tk.END)
            self.duracao_servico.delete(0, tk.END)
            self.var.set(0)

    def create_treeview(self):
        # LabelFrame for Treeview
        self.frame_lista = tk.LabelFrame(self, text="Lista de Serviços", bg="#b4918f", fg="white", font=('TkMenuFont', 12))
        self.frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree_frame = tk.Frame(self.frame_lista, bg="#b4918f")
        self.tree_frame.pack(pady=(20, 0), fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nome", "Preço", "Duração", "Status", "Cargo"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Preço", text="Preço")
        self.tree.heading("Duração", text="Duração")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Cargo", text="Cargo")

        self.tree.column("ID", width=30)
        self.tree.column("Nome", width=150)
        self.tree.column("Preço", width=100)
        self.tree.column("Duração", width=100)
        self.tree.column("Status", width=100)
        self.tree.column("Cargo", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_services(self):
        self.tree.delete(*self.tree.get_children())
        for service in dados.db_listar_servico():
            selected_cargo = service["id_cargo"]
            nome_cargo = self.cargo_map_inverse.get(selected_cargo)
            # status = "ativo" if service["status"] == 2 else "inativo"
            self.tree.insert("", "end", values=(service["id_servico"], service["nome_servico"], service["preco_servico"], service["duracao_servico"], service["status"], nome_cargo))


    def buscar_servico(self):
        quandro2 = tk.LabelFrame(self, text="Pesquisar Serviço", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quandro2.pack(fill="both", expand=True, padx=10, pady=10)

        self.pNome = tk.Entry(quandro2)
        self.pNome.bind('<Return>', (lambda event: self.pesquisaCliente()))
        self.pNome.pack(side="left", padx=10)

        tk.Button(quandro2, text="Pesquisar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.pesquisaCliente).pack(side="left", padx=10)

        tk.Button(quandro2, text="Mostrar Todos", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=lambda: self.load_services()).pack(side="left", padx=10)

        tk.Button(quandro2, text="Atualizar/Deletar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.atualizar_deletar).pack(side="left", padx=10)
        
    def pesquisaCliente(self):
        self.tree.delete(*self.tree.get_children())
        services = dados.db_listar_nome_servico(self.pNome.get())
        self.pNome.delete(0, tk.END)
        for service in services:
            status = "ativo" if service["status"] == 1 else "inativo"
            self.tree.insert("", "end", values=(service["id_servico"], service["nome_servico"], service["preco_servico"], service["duracao_servico"], status))

    def atualizar_deletar(self):
        try:
            itemSelecionado = self.tree.selection()[0]
            valores = self.tree.item(itemSelecionado, "value")
            from servico.update_servico import Update_servico
            Update_servico(self.master, valores)      
            self.destroy() 
            
        except:
            showinfo("ERRO","Selecione o Serviço a ser Atualizado", parent=self)
