import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno
from tkcalendar import DateEntry

class Update_Funcionario(tk.Toplevel):
    def __init__(self, parent, valores):
        super().__init__(parent)

        self.valores = valores
       
    
        self.title("Atualizar/Deletar Funcionário")
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
        self.frame_cadastro = tk.LabelFrame(self, text="Atualizar/Deletar Funcionário", bg="#b4918f", fg="white", font=('TkMenuFont', 12))
        self.frame_cadastro.pack(padx=10, pady=100, fill="both", expand=False)

        # Create a frame to hold the form
        form_frame = tk.Frame(self.frame_cadastro, bg="#b4918f")
        form_frame.pack(pady=10, padx=10)

        # Nome do Funcionário
        tk.Label(form_frame, text="Nome do Funcionário", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=0, column=0, pady=2, sticky='e')
        self.nome_funcionario = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.nome_funcionario.grid(row=0, column=1, pady=2, padx=5)
        self.nome_funcionario.insert(0, self.valores[1])

        # CPF
        tk.Label(form_frame, text="CPF", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=1, column=0, pady=2, sticky='e')
        vcmd = (self.register(self.validate_cpf), '%P')
        self.cpf_funcionario = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10), validate='key', validatecommand=vcmd)
        self.cpf_funcionario.grid(row=1, column=1, pady=2, padx=5)
        self.cpf_funcionario.insert(0, self.valores[2])

        # Email
        tk.Label(form_frame, text="Email", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=2, column=0, pady=2, sticky='e')
        self.Email_funcionario = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.Email_funcionario.grid(row=2, column=1, pady=2, padx=5)
        self.Email_funcionario.insert(0, self.valores[3])

        # Endereço
        tk.Label(form_frame, text="Endereço", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=3, column=0, pady=2, sticky='e')
        self.endereco = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.endereco.grid(row=3, column=1, pady=2, padx=5)
        self.endereco.insert(0, self.valores[4])

        # Telefone
        tk.Label(form_frame, text="Telefone", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=4, column=0, pady=2, sticky='e')
        self.telefone = tk.Entry(form_frame, width=30, font=('TkMenuFont', 10))
        self.telefone.grid(row=4, column=1, pady=2, padx=5)
        self.telefone.insert(0, self.valores[5])

        status_doc = [{'id': 1, 'nome':"ativo"}, {"id":0,"nome":"inativo"}]
        status_map = {c['nome']: c['id'] for c in status_doc}
        status_id = status_map[self.valores[7]]

        # Checkbox
        tk.Label(form_frame, text="Status", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=5, column=0, pady=2, sticky='e')
        self.var = tk.IntVar(value=status_id)
        checkbox = tk.Checkbutton(form_frame, text="Ativo", variable=self.var, onvalue=1, offvalue=0, bg="#b4918f")
        checkbox.grid(row=5, column=1, pady=2, sticky='w')

        # Cargo Combobox
        tk.Label(form_frame, text="Cargo", bg="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=5, column=2, pady=2, sticky='e')
        cargo = dados.db_listar_cargo()
        self.cargo_map = {c['nome_cargo']: c['id_cargo'] for c in cargo}
        cargo_names = list(self.cargo_map.keys())
        self.textArea = ttk.Combobox(form_frame, values=cargo_names)
        self.textArea.grid(row=5, column=3, pady=2, padx=5, sticky='w')
        self.textArea.insert(0,self.valores[6])
        

        # Cadastrar Button
        
        tk.Button(form_frame, text="Atualizar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.editar_funcionario).grid(row=6, column=0, pady=10, sticky='w')
        
        tk.Button(form_frame, text="Deletar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black", bd=5, command=self.deletar_funcionario).grid(row=6, column=3, pady=10, sticky='e')
        


    def editar_funcionario(self):
        estado = "ativo" if self.var.get() == 1 else "inativo"
        
        if self.nome_funcionario.get() == "" or self.cpf_funcionario.get() == "" or self.Email_funcionario.get() == "" or self.textArea.get() == "":
            return showinfo(title=False, message="Preencha todos os campos", parent=self)
        
        selected_cargo = self.textArea.get()
        if selected_cargo in self.cargo_map:
            selected_id_cargo = self.cargo_map[selected_cargo]

        s = dados.editar_funcionario(self.valores[0], self.nome_funcionario.get().strip(" ").capitalize(), self.Email_funcionario.get(), self.endereco.get(), self.cpf_funcionario.get(), self.telefone.get(), selected_id_cargo, estado)
        if s == False:
            self.nome_funcionario.delete(0, tk.END)
            self.cpf_funcionario.delete(0, tk.END)
            self.Email_funcionario.delete(0, tk.END)
            self.endereco.delete(0, tk.END)
            self.telefone.delete(0, tk.END)
            return showinfo(title=False, message="Funcionário Já existe", parent=self)
            
        else:
            showinfo(title=False, message="Atualizado com sucesso", parent=self)
            self.destroy()
            from funcionario.funcionario import Funcionario
            Funcionario(self.master)
            

    def deletar_funcionario(self):
        confirm = askyesno(title="Confirmar", message="Você tem certeza que deseja deletar este funcionário?", parent=self)
        if confirm:
            self.executar_delecao()
        else:
            showinfo(title="Cancelado", message="Operação de deleção cancelada", parent=self)

    def executar_delecao(self):
        try:
            
            dados.apagar_funcionario(self.valores[0])
            showinfo(title="Sucesso", message="Funcionário deletado com sucesso", parent=self)
            self.destroy()
            from funcionario.funcionario import Funcionario
            Funcionario(self.master)
        except Exception as e:
            showinfo(title="Erro", message=f"Erro ao deletar funcionário: {e}", parent=self)




    def validate_cpf(self, new_value):
        # Verifica se o novo valor contém apenas dígitos e tem no máximo 11 caracteres
        return new_value.isdigit() and len(new_value) <= 11