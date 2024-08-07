import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion

# from maskedentry import*
from tkcalendar import DateEntry
from operator import neg
# import calendario


class Forma_Pagamento(tk.Toplevel):
  
  def __init__(self, master, valor, callback):
    super().__init__(master)
    


    self.master = master
    self.callback = callback
    self.formaPag = []
    
    self.title("Forma de Pagamento")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 8
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('800x400+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")
    
    
    
    
    self.tvc = ttk.Treeview(self, columns=("id","valor","forma de pagamento"), show="headings",)
    self.tvc.column("id",minwidth=0,width=50, anchor=tk.CENTER)
    self.tvc.column("valor",minwidth=0,width=250, anchor=tk.CENTER)
    self.tvc.column("forma de pagamento",minwidth=0,width=100, anchor=tk.CENTER)
    self.tvc.heading("id", text="ID")
    self.tvc.heading("valor", text="VALOR")
    self.tvc.heading("forma de pagamento", text="FORMA DE PAGAMENTO")
    self.tvc.configure(height=4)
    self.tvc.pack(fill="both",expand="no", padx=2,pady=10,)
    
    
    tk.Label(
        self,
        text="Valor Total",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 9)
        ).pack(side="left")
    self.segundaFo = tk.DoubleVar()

    # self.result_label = ttk.Label(self, text="")
    # self.result_label.pack(pady=10)

    self.vcmd = (self.register(self.validate_entry), '%P')

    self.forma2 =tk.Entry(self, width=8, textvariable=self.segundaFo, validate="key", validatecommand= self.vcmd)
    self.forma2.pack(side="left",padx=10)
    
    #comboBox = ttk.Combobox(app, values=lista, width=10)
    #comboBox.pack(side="left",padx=10)
    self.segundaFo.set(valor)
    
    
    formaPagamneto = dados.db_listar_forma_pagamento()
    lista = []
    for f in formaPagamneto:
        lista.append(f['nome'])
        
    tk.Label(
            self,
            text="Valor Parcial",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left")
    
    self.primeiraF = tk.DoubleVar()

    self.forma1 =tk.Entry(self, width=8, textvariable=self.primeiraF, validate="key", validatecommand= self.vcmd)
    self.forma1.pack(side="left",padx=10)
    self.forma1.bind("<KeyRelease>", self.calcForma)
    
    
    tk.Label(
            self,
            text="Valor Restante",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left")
    
    self.segundaF = tk.DoubleVar()

    self.forma3 =tk.Entry(self, width=8, textvariable=self.segundaF, validate="key", validatecommand= self.vcmd)
    self.forma3.pack(side="left",padx=10)
    
    tk.Label(
        self,
        text="Forma de Pagamento",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 9)
        ).pack(side="left")
    
    
    self.comboBox = ttk.Combobox(self, values=lista, width=10)
    self.comboBox.pack(side="left",padx=10)
    
    tk.Button(
    self,
    text=("Adicionar"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.adicionarForma()).pack(side="left")
    
    tk.Button(
    self,
    text=("Finalizar "),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.return_data()).place(x=300, y=300)


    
    
    
    
    self.focus_force()
    self.grab_set()
    self.forma2.focus()

  def fechar(self):
    self.destroy()
    return self.formaPag
  

  def adicionarForma(self):
    id = 0
    listaF = [self.forma1.get(), self.comboBox.get()]
    self.formaPag.append(listaF)
    formaPagmanemto = dados.db_listar_forma_pagamento()
    for f in formaPagmanemto:
        if self.comboBox.get() == f["nome"]:
            id = f["id_forma_pagamento"]
          
    self.tvc.insert("","end", values=(id,self.forma1.get(), self.comboBox.get()))
    self.segundaFo.set(self.forma3.get())
    self.primeiraF.set("0.00")
        
        
        
  def calcForma(self,e):
    self.segundaF.set(float(self.segundaFo.get()) - float(self.forma1.get()))



  def validate_entry(self, new_value):
        # Verifica se a entrada é um número inteiro
        if new_value.isdigit() or new_value == "":
            
            return True
        else:
            
            return False  
        

  def return_data(self):
        
        # Obter dados do Entry e passar para a função de callback
        data = self.formaPag
        self.callback(data)
        self.destroy()
        

    

        
  
    
        
        
          
    
