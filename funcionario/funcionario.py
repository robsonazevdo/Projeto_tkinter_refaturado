import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkcalendar import DateEntry

class Funcionario(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Cadastrar Funcionário")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = self.winfo_screenwidth() // 10
        y = int(self.winfo_screenheight() * 0.03)
        self.geometry('1000x690+' + str(x) + '+' + str(y))
        self.configure(background="#b4918f")

        self.create_treeview()
        self.create_widgets()
        self.buscar_servico()
        self.load_oficials()
        
        self.transient()
        self.focus_force()
        self.grab_set()

    def create_widgets(self):
        self.frame_cadastro = tk.LabelFrame(self, text="Cadastrar Funcionário", bg="#b4918f", fg="white", font=('TkMenuFont', 12))
        self.frame_cadastro.pack(padx=10, pady=10, fill="both", expand=False)

        # Create a frame to hold the form
        form_frame = tk.Frame(self.frame_cadastro, bg="#b4918f")
        form_frame.pack(pady=10, padx=10)

        # Nome do Funcionário
        tk.Label(form_frame, text="Nome do Funcionário", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=0, column=0, pady=2, sticky='e')
        self.nome_funcionario = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.nome_funcionario.grid(row=0, column=1, pady=2, padx=5)

        # CPF
        tk.Label(form_frame, text="CPF", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=1, column=0, pady=2, sticky='e')
        vcmd = (self.register(self.validate_cpf), '%P')
        self.cpf_funcionario = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10), validate='key', validatecommand=vcmd)
        self.cpf_funcionario.grid(row=1, column=1, pady=2, padx=5)

        # Email
        tk.Label(form_frame, text="Email", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=2, column=0, pady=2, sticky='e')
        self.Email_funcionario = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.Email_funcionario.grid(row=2, column=1, pady=2, padx=5)

        # Endereço
        tk.Label(form_frame, text="Endereço", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=3, column=0, pady=2, sticky='e')
        self.endereco = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.endereco.grid(row=3, column=1, pady=2, padx=5)

        # Telefone
        tk.Label(form_frame, text="Telefone", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=4, column=0, pady=2, sticky='e')
        self.telefone = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.telefone.grid(row=4, column=1, pady=2, padx=5)

        # Checkbox
        tk.Label(form_frame, text="Status", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=5, column=0, pady=2, sticky='e')
        self.var = tk.IntVar()
        checkbox = tk.Checkbutton(form_frame, text="Ativo", variable=self.var, onvalue=1, offvalue=2, bg="#b4918f")
        checkbox.grid(row=5, column=1, pady=2, sticky='w')

        # Cargo Combobox
        tk.Label(form_frame, text="Cargo", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=5, column=2, pady=2, sticky='e')
        cargo = dados.db_listar_cargo()
        self.cargo_map = {c['nome_cargo']: c['id_cargo'] for c in cargo}
        cargo_names = list(self.cargo_map.keys())
        self.cargo_map_inverse = {v: k for k, v in self.cargo_map.items()}
        self.textArea = ttk.Combobox(form_frame, values=cargo_names)
        self.textArea.grid(row=5, column=3, pady=2, padx=5, sticky='w')


        # Cadastrar Button
        tk.Button(form_frame, text="Cadastrar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.criar_servico).grid(row=6, column=1, pady=10, sticky='w')

        
    def criar_servico(self):
        estado = "ativo" if self.var.get() == 1 else "inativo"
        
        if self.nome_funcionario.get() == "" or self.cpf_funcionario.get() == "" or self.Email_funcionario.get() == "" or self.textArea.get() == "":
            return showinfo(title=False, message="Preencha todos os campos", parent=self)
        
        selected_cargo = self.textArea.get()
        if selected_cargo in self.cargo_map:
            selected_id_cargo = self.cargo_map[selected_cargo]
            
        ja_existe, s = dados.criar_funcionario(selected_id_cargo, self.nome_funcionario.get().strip(" ").capitalize(), self.cpf_funcionario.get(), self.Email_funcionario.get(), self.endereco.get(), self.telefone.get(), estado)
        if ja_existe != False:
            self.nome_funcionario.delete(0, tk.END)
            self.cpf_funcionario.delete(0, tk.END)
            self.Email_funcionario.delete(0, tk.END)
            self.endereco.delete(0, tk.END)
            self.telefone.delete(0, tk.END)
            return showinfo(title=False, message="Funcionário Já existe", parent=self)
            
        else:
            showinfo(title=False, message="Cadastro feito com sucesso", parent=self)
            self.load_oficials()
            self.nome_funcionario.delete(0, tk.END)
            self.cpf_funcionario.delete(0, tk.END)
            self.Email_funcionario.delete(0, tk.END)
            self.endereco.delete(0, tk.END)
            self.telefone.delete(0, tk.END)
            self.var.set(0)

    def create_treeview(self):
        # LabelFrame for Treeview
        self.frame_lista = tk.LabelFrame(self, text="Lista de Funcionários", bg="#b4918f", fg="white", font=('TkMenuFont', 12))
        self.frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree_frame = tk.Frame(self.frame_lista, bg="#b4918f")
        self.tree_frame.pack(pady=(10, 0), fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nome", "CPF", "Email", "Endereço", "Telefone","Função", "Status"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Função", text="Função")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=30)
        self.tree.column("Nome", width=100)
        self.tree.column("CPF", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Endereço", width=150)
        self.tree.column("Telefone", width=100)
        self.tree.column("Função", width=50)
        self.tree.column("Status", width=80)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_oficials(self):
        self.tree.delete(*self.tree.get_children())
        for oficial in dados.db_listar_funcionarios():
            selected_cargo = oficial["id_cargo"]
            nome_cargo = self.cargo_map_inverse.get(selected_cargo)

                
            self.tree.insert("", "end", values=(oficial["id_funcionario"], oficial["nome"], oficial["cpf"], oficial["email"], oficial["endereco"], oficial["telefone"],nome_cargo , oficial["status"]))


    def buscar_servico(self):
        quandro2 = tk.LabelFrame(self, text="Pesquisar Funcionário", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quandro2.pack(fill="both", expand=False, padx=10, pady=10)

        self.pNome = tk.Entry(quandro2)
        self.pNome.bind('<Return>', (lambda event: self.pesquisarFuncionario()))
        self.pNome.pack(side="left", padx=10)

        tk.Button(quandro2, text="Pesquisar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.pesquisarFuncionario).pack(side="left", padx=10)

        tk.Button(quandro2, text="Mostrar Todos", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=lambda: self.load_oficials()).pack(side="left", padx=10)
        
        tk.Button(quandro2, text="Atualizar/Deletar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.atualizar_deletar).pack(side="left", padx=10)


    def pesquisarFuncionario(self):
        self.tree.delete(*self.tree.get_children())
        oficials = dados.db_listar_nome_funcionario(self.pNome.get())
        self.pNome.delete(0, tk.END)
        for oficial in oficials:
            selected_cargo = oficial["id_cargo"]
            if selected_cargo in self.cargo_map:
                selected_id_cargo = self.cargo_map[selected_cargo]
            print(selected_id_cargo)
            self.tree.insert("", "end", values=(oficial["id_funcionario"], oficial["nome"], oficial["cpf"], oficial["email"], oficial["endereco"], oficial["telefone"], selected_id_cargo, oficial["status"]))

    def validate_cpf(self, new_value):
        # Verifica se o novo valor contém apenas dígitos e tem no máximo 11 caracteres
        return new_value.isdigit() and len(new_value) <= 11
    
    
    def atualizar_deletar(self):
        try:
            from funcionario.update_funcionario import Update_Funcionario
            itemSelecionado = self.tree.selection()[0]
            valores = self.tree.item(itemSelecionado, "value")
            Update_Funcionario(self.master, valores)      
            self.destroy() 
            
        except:
            showinfo("ERRO","Selecione o Funciánario a ser Atualizado", parent=self)