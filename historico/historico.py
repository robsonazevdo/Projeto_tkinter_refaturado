import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion
from tkcalendar import DateEntry
from operator import neg
from datetime import datetime, date


class Historico_Atendimento(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)

    
    
    self.title("Histórico Atendimento")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 8
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('1000x600+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")
    
    
    
    quadroGrid = tk.LabelFrame(self, text="Atendimentos", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
    quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
    
    self.tv = ttk.Treeview(quadroGrid, columns=("Comanda", "Data Venda", "Valor Total", "Desconto", "Forma Pagamento", "Serviço", "Quantidade"), show='headings')
    
    self.tv.heading("Comanda", text="Comanda Nº")
    self.tv.heading("Data Venda", text="Data da Venda")
    self.tv.heading("Valor Total", text="Valor Total")
    self.tv.heading("Desconto", text="Desconto")
    self.tv.heading("Forma Pagamento", text="Forma de Pagamento")
    self.tv.heading("Serviço", text="Serviço")
    self.tv.heading("Quantidade", text="Quantidade")

    
    self.tv.column("Comanda", width=100)
    self.tv.column("Data Venda", width=100)
    self.tv.column("Valor Total", width=100)
    self.tv.column("Desconto", width=100)
    self.tv.column("Forma Pagamento", width=150)
    self.tv.column("Serviço", width=150)
    self.tv.column("Quantidade", width=100)
    self.tv.pack()
      
          
    
    
    btn_carregar = tk.Button(quadroGrid, text="Carregar Histórico", font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    command=self.mostrar_historico_atendimento)
    btn_carregar.pack(pady=10)

    self.quadroGrid = tk.LabelFrame(self, text="Clientes", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
    self.quadroGrid.pack(fill="both", padx=10,pady=10)
    
    self.tv2 = ttk.Treeview(self.quadroGrid, columns=("id","Nome"), show="headings",)
    
    self.tv2.column("id",minwidth=0,width=30, anchor=tk.W, )
    
    self.tv2.column("Nome",minwidth=15,width=150, anchor=tk.W)
    
    self.tv2.heading("id", text="ID", anchor=tk.W)
    
    self.tv2.heading("Nome", text="NOME", anchor=tk.W)
    
    self.tv2.pack()
    self.popular()
    
    self.focus_force()
    self.grab_set()
    

        
  def mostrar_historico_atendimento(self):

    try:
        
        if not self.tv2.selection():
            showerror("ERRO!", "Precisa Selecionar um Cliente", parent=self)
            return
        

        items = self.tv2.selection()[0]
        cliente = self.tv2.item(items, "value")
    
    
    
        resultados = dados.obter_historico_atendimento(cliente[1])
        
        
        if not resultados:
            showinfo("Histórico de Atendimento", f"Sem histórico de atendimento para o cliente: {cliente[1]}", parent=self)
            return
        
        
        self.tv.delete(*self.tv.get_children())

        
        comanda_atual = None

        
        for f in resultados:
          numero_comanda = f["numero_comanda"]
          data_obj = datetime.strptime(f["data_venda"], "%Y-%m-%d %H:%M:%S")
          data_venda = data_obj.strftime("%d/%m/%Y")
          valor_total = f["valor_total"]
          desconto = f["desconto"]
          forma_pagamento = f["forma_pagamento"]
          nome_servico = f["nome_servico"]
          quantidade = f["quantidade"]
          
          if comanda_atual != numero_comanda:
              
              self.tv.insert("", "end", values=(numero_comanda, data_venda, valor_total, desconto, forma_pagamento, nome_servico, quantidade))
              comanda_atual = numero_comanda
          else:
              
              self.tv.insert("", "end", values=("", "", "", "", "", nome_servico, quantidade))

    except Exception as e:
        showerror("ERRO!", f"Um erro ocorreu: {str(e)}", parent=self)

        
  def popular(self):
    self.tv2.delete(*self.tv.get_children())
    cliente = dados.db_listar_cliente()
    
    for c in cliente:
        self.tv2.insert("","end", values=(c['id_cliente'],c['nome']))        