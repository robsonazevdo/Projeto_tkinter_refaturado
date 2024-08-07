import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

# from maskedentry import*
from tkcalendar import DateEntry
from operator import neg
# import calendario


class Pesquisar_Cliente(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)

   
    self.title("Pesquisar Cliente")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 4
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('700x500+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")
    
    quadroGrid = tk.LabelFrame(self, text="Clientes", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
    quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
    
    self.tv = ttk.Treeview(quadroGrid, columns=("id","nome","fone"), show="headings",)
    self.tv.column("id",minwidth=0,width=50)
    self.tv.column("nome",minwidth=0,width=250)
    self.tv.column("fone",minwidth=0,width=100)
    self.tv.heading("id", text="ID")
    self.tv.heading("nome", text="NOME")
    self.tv.heading("fone", text="TELEFONE")
    self.tv.pack()
    
    self.popular(self.tv)

    quandro1 = tk.LabelFrame(self, text = "Inserir Novos Clientes", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
    quandro1.pack(fill="both", expand='yes',padx=10, pady=10)

    tk.Label(
            quandro1,
            text="Nome cliente",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 12),
            bd=5,
            ).pack(side="left")
        
    self.nome_cliente =tk.Entry(quandro1)
    self.nome_cliente.pack(side="left",padx=10)
    
    tk.Label(
            quandro1,
            text="Telefone",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 12),
            ).pack(side="left")
        
    self.fone =tk.Entry(quandro1)
    self.fone.pack(side="left",padx=10)
    
    

    tk.Button(
    quandro1,
    text=("Inserir"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.inserir(self.nome_cliente.get(), self.fone.get())).pack(side="left",padx=10)
    
    
    
    quandro2 = tk.LabelFrame(self, text = "Pesquisar Clientes",  background="#b4918f", fg="white",bd=5, font=('TkMenuFont', 12))
    quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

        
    self.pNome =tk.Entry(quandro2)
    self.pNome.bind('<Return>', (lambda event: self.pesquisaCliente(self.tv, self.pNome.get())))
    self.pNome.pack(side="left",padx=10)
    
    tk.Button(
    quandro2,
    text=("Pesquisar"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.pesquisaCliente(self.tv, self.pNome.get())).pack(side="left",padx=10)
    
    

    tk.Button(
    quandro2,
    text=("Mostrar Todos"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.popular(self.tv)).pack(side="left",padx=10)


    tk.Button(
    quandro2,
    text=("Atualizar/Deletar Cliente"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.update_cliente()).pack(side="left",padx=10)
    
    
    self.focus_force()
    self.grab_set()




  def inserir(self,nome_cliente,fone):
    if nome_cliente == "" or fone == "":
        return showinfo(title=False, message="Preencha todos os campos",  parent=self)
        
    ja_existe, c = dados.criar_cliente(self.nome_cliente.get(),self.fone.get())
    if ja_existe != False:
        self.nome_cliente.delete(0,tk.END)
        self.fone.delete(0,tk.END)
        return showinfo(title=False, message="Cliente Já existe",  parent=self)
        
    else:
        showinfo(title=False, message="Cadastro feito com sucesso",  parent=self)
        self.nome_cliente.delete(0,tk.END)
        self.fone.delete(0,tk.END)
        self.popular(self.tv)
        return
    


  def popular(self,tv):
        tv.delete(*tv.get_children())
        cliente = dados.db_listar_cliente()

        for c in cliente:
            tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
                


  def pesquisaCliente(self,tv, nome):

    tv.delete(*tv.get_children())
    historico = dados.db_historico_cliente(nome)
    self.pNome.delete(0,tk.END)
    for c in historico:
        tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
                

  def update_cliente(self):
    
    try:
      from cliente.update_cliente import Update_Cliente
      itemSelecionado = self.tv.selection()[0]
      valores = self.tv.item(itemSelecionado, "value")
      Update_Cliente(self.master,valores)      
      self.destroy() 
        
    except:
        showinfo("ERRO","Selecione o Cliente a ser Atualizado", parent=self)
         
        
        
        
        
        
        