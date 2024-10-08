import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno
from tkcalendar import DateEntry

class Update_servico(tk.Toplevel):
    def __init__(self, parent, valores):
        super().__init__(parent)

        self.valores = valores
        

        self.title("Editar/Deletar Serviço")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = self.winfo_screenwidth() // 10
        y = int(self.winfo_screenheight() * 0.03)
        self.geometry('1000x690+' + str(x) + '+' + str(y))
        self.configure(background="#b4918f")

        
        self.create_widgets()
        
        
        
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
        self.nome_servico.insert(0,self.valores[1])

        # Preço Serviço
        tk.Label(form_frame, text="Preço Serviço", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=1, column=0, pady=5, sticky='e')
        self.preco_servico = tk.Entry(form_frame, width=65, font=('TkMenuFont', 10))
        self.preco_servico.grid(row=1, column=1, pady=5, padx=10)
        self.preco_servico.insert(0,self.valores[2])

        # Duração Serviço
        tk.Label(form_frame, text="Duração Serviço", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=2, column=0, pady=5, sticky='e')
        self.duracao_servico = tk.Entry(form_frame, width=65, font=('TkMenuFont', 10))
        self.duracao_servico.grid(row=2, column=1, pady=5, padx=10)
        self.duracao_servico.insert(0,self.valores[3])


        status_doc = [{'id': 1, 'nome':"ativo"}, {"id":0,"nome":"inativo"}]
        status_map = {c['nome']: c['id'] for c in status_doc}
        status_id = status_map[self.valores[4]]

        # Checkbox
        tk.Label(form_frame, text="Status", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=3, column=0, pady=5, sticky='e')
        self.var = tk.IntVar(value=status_id)
        checkbox = tk.Checkbutton(form_frame, text="Ativo", variable=self.var, onvalue=1, offvalue=0, bg="#b4918f")
        checkbox.grid(row=3, column=1, pady=5, sticky='w')

        # Cargo Combobox
        tk.Label(form_frame, text="Quem Realiza?", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=3, column=1, pady=5, sticky='e')
        cargo = dados.db_listar_cargo()
        self.cargo_map = {c['nome_cargo']: c['id_cargo'] for c in cargo}
        cargo_names = list(self.cargo_map.keys())
        self.textArea = ttk.Combobox(form_frame, values=cargo_names)
        self.textArea.grid(row=3, column=2, pady=5, padx=10, sticky='w')
        self.textArea.insert(0,self.valores[5])

        # Editar Button
        tk.Button(form_frame, text="Editar ", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.editar_servico).grid(row=5, column=1, pady=20, sticky='w')
        

        # Deletar Button
        tk.Button(form_frame, text="Deletar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.deletar_servico).grid(row=5, column=2, pady=20, sticky='w')

    def editar_servico(self):
        estado = "ativo" if self.var.get() == 1 else "inativo"
        
        if self.nome_servico.get() == "" or self.preco_servico.get() == "" or self.duracao_servico.get() == "" or self.textArea.get() == "":
            return showinfo(title=False, message="Preencha todos os campos", parent=self)
        
        selected_cargo = self.textArea.get()
        if selected_cargo in self.cargo_map:
            selected_id_cargo = self.cargo_map[selected_cargo]
        s = dados.editar_servico(self.valores[0], self.nome_servico.get().strip(" ").capitalize(), self.preco_servico.get(), self.duracao_servico.get(), estado, selected_id_cargo)
        if s == False:
            self.nome_servico.delete(0, tk.END)
            self.preco_servico.delete(0, tk.END)
            self.duracao_servico.delete(0, tk.END)
            return showinfo(title=False, message="Serviço Já existe", parent=self)
            
        else:
            showinfo(title=False, message="Atualizado com sucesso", parent=self)
            self.destroy()
            from servico.servico import Servico
            Servico(self.master)


    def deletar_servico(self):
        confirm = askyesno(title="Confirmar", message="Você tem certeza que deseja deletar este serviço?", parent=self)
        if confirm:
            self.executar_delecao()
        else:
            showinfo(title="Cancelado", message="Operação de deleção cancelada", parent=self)


    def executar_delecao(self):
        try:
            
            dados.apagar_servico(self.valores[0])
            showinfo(title="Sucesso", message="Serviço deletado com sucesso", parent=self)
            self.destroy()
            from servico.servico import Servico
            Servico(self.master)
        except Exception as e:
            showinfo(title="Erro", message=f"Erro ao deletar Serviço: {e}", parent=self)
