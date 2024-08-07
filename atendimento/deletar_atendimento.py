import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion
from tkcalendar import DateEntry
from operator import neg
# import calendario


class Deletar_Atendimento(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)

    
    
    self.title("Excluir Atendimento")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 8
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('1000x600+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")
    
    
    
    quadroGrid = tk.LabelFrame(self, text="Atendimentos", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
    quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
    
    self.tv = ttk.Treeview(quadroGrid, columns=("id","Data","Nome","Valor", "Descricao", "Desconto","Valor_Pago", "forma"), show="headings",)
    self.tv.column("id",minwidth=15,width=50)
    self.tv.column("Data",minwidth=15,width=70)
    self.tv.column("Nome",minwidth=15,width=250)
    self.tv.column("Valor",minwidth=15,width=100)
    self.tv.column("Descricao",minwidth=50,width=250)
    self.tv.column("Desconto",minwidth=0,width=100)
    self.tv.column("Valor_Pago",minwidth=0,width=100)
    self.tv.column("forma",minwidth=0,width=100)
    self.tv.heading("id", text="ID")
    self.tv.heading("Data", text="DATA")
    self.tv.heading("Nome", text="NOME")
    self.tv.heading("Valor", text="VALOR")
    self.tv.heading("Descricao", text="DESCRIÇÃO")
    self.tv.heading("Desconto", text="DESCONTO")
    self.tv.heading("Valor_Pago", text="VALOR PAGO")
    self.tv.heading("forma", text="FORMA DE PAGAMENTO")
    self.tv.pack()
    self.popular()
      
          
    
    
    quandro2 = tk.LabelFrame(self, text = "Pesquisar Clientes",  background="#b4918f", fg="white",bd=5, font=('TkMenuFont',12))
    quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

        
    self.pNome =tk.Entry(quandro2)
    self.pNome.bind('<Return>', (lambda event: self.buscarAtendimento()))
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
    
    command=lambda: self.buscarAtendimento()).pack(side="left",padx=10)
    
    

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
    
    command=lambda: self.popular()).pack(side="left",padx=10)
    
    tk.Button(
    quandro2,
    text=("Excluir Atendimento"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.deletar()).pack(side="left",padx=10)
    
    self.focus_force()
    self.grab_set()
    

  def deletar(self):
    try:
        itemS = self.tv.selection()[0]
        valores = self.tv.item(itemS,"value")
        msg = askquestion("?","Deseja Excluir o Atendimento do Cliente {0} do dia {1}".format(valores[2], valores[1]), parent=self )
        if msg == "yes":
            dados.db_deletar_atendimento(valores[0])
            showinfo("Sucesso", "Cadastro foi excluíndo com sucesso", parent=self)
            self.destroy()
                    
                
    except:
          showerror("ERRO!", "Precisa Selecionar um item", parent=self)
                
  def buscarAtendimento(self):
      self.tv.delete(*self.tv.get_children())
      historico = dados.db_historico_atendimento(self.pNome.get())
      self.pNome.delete(0,tk.END)
      for c in historico:
        self.tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_unitario'], c['descricao'],"%.2f" %c['desconto'],"%.2f" %c['valor_total'],c['forma_pagamento']))
          
        
  def popular(self):
      self.tv.delete(*self.tv.get_children())
      cliente = dados.db_listar_atendimento()
  
      for c in cliente:
        self.tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_unitario'], c['descricao'],"%.2f" %c['desconto'],"%.2f" %c['valor_total'],c['forma_pagamento']))        
          