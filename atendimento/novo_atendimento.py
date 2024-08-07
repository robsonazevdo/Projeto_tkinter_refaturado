import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion
from atendimento.forma_pagamento import Forma_Pagamento
# from maskedentry import*
from tkcalendar import DateEntry
from operator import neg
# import calendario
from datetime import datetime, date


class Novo_Atendimento(tk.Toplevel):
  def __init__(self, master, callback):
    super().__init__(master)

    self.options = []
    
           
    self.master = master
    self.callback = callback
    
    self.title("Novo Atendimento")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 10
    y = int(self.winfo_screenheight() * 0.03)
    self.geometry('1000x690+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")
    
    vcmd = self.register(func=self.limitar_tamanho)
    
    
    self.quadroGrid = tk.LabelFrame(self, text="Clientes", background="#b4918f", fg="white", bd=5,font=('TkMenuFont', 12))
    self.quadroGrid.configure(height=3)
    self.quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)

    
    
    self.tv = ttk.Treeview(self.quadroGrid, columns=("id","nome","fone"), show="headings",)
    self.tv.column("id",minwidth=0,width=50, anchor=tk.CENTER)
    self.tv.column("nome",minwidth=0,width=250, anchor=tk.CENTER)
    self.tv.column("fone",minwidth=0,width=100, anchor=tk.CENTER)
    self.tv.heading("id", text="ID")
    self.tv.heading("nome", text="NOME")
    self.tv.heading("fone", text="TELEFONE")
    self.tv.configure(height=1)
    self.tv.pack(fill="both",expand="yes", padx=10,pady=10,)
    self.popular()
    
    self.quadroGrid2 = tk.LabelFrame(self, text="Adicionar Atendimentos", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
    self.quadroGrid2.pack(fill="both",expand="yes", padx=10,pady=10)
            
    self.tv2 = ttk.Treeview(self.quadroGrid2, columns=("item","Descricao","Valor","Total"), show="headings",)
    self.tv2.configure(height=2)
    self.tv2.column("item",minwidth=0,width=80, anchor=tk.CENTER)
    self.tv2.column("Descricao",minwidth=15,width=250,anchor=tk.CENTER)
    self.tv2.column("Valor",minwidth=15,width=100,anchor=tk.CENTER)
    self.tv2.column("Total",minwidth=15,width=100,anchor=tk.CENTER)
    
    
    
    self.tv2.heading("item", text="QUANTIDADE")
    self.tv2.heading("Descricao", text="DESCRIÇÃO")
    self.tv2.heading("Valor", text="VALOR")
    self.tv2.heading("Total", text="TOTAL")
    self.tv2.pack(fill="both",expand="yes", padx=10,pady=10)
    
    self.quadro = tk.LabelFrame(self, text = "Serviço Realizado", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
    self.quadro.configure(height=2)
    self.quadro.pack(fill="both", expand='yes',padx=10, pady=10)
    
    tk.Label(
            self.quadroGrid2,
            text="Data Realizada",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=10)
    
    

    
    self.data = DateEntry(self.quadroGrid2, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
    
    self.data.pack(side="left",padx=10)
    
    
    
    tk.Label(
            self.quadroGrid2,
            text="Quantidade",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=10)
    
    
    
    self.qta = tk.Entry(self.quadroGrid2)
    self.qta.pack(side="left",padx=10)
    
    tk.Label(
        self.quadroGrid2,
        text="Descrição",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 9)
        ).pack(side="left", pady=10)

    service = dados.db_listar_servico()
    self.service_map = {serv['nome_servico']: serv['preco_servico'] for serv in service}
    service_names = list(self.service_map.keys())

    self.textArea = ttk.Combobox(self.quadroGrid2, values=service_names)
    self.textArea.pack(side="left",padx=10)

    self.textArea.bind("<<ComboboxSelected>>", self.update_preco_service)



    tk.Label(
            self.quadroGrid2,
            text="Valor",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=10,padx=10)
    
    self.lb_valor = tk.DoubleVar()   
    self.valor =tk.Entry(self.quadroGrid2, width=8, textvariable=self.lb_valor, validate="key", validatecommand=(vcmd, "%P"))
    self.valor.pack(side="left",padx=10)
    
    
    
    tk.Button(
    self.quadroGrid2,
    text=("Inserir"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.adicionarServico()).pack(side="left") 
    
    tk.Button(
    self.quadroGrid2,
    text=("Deletar"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.deletar()).pack(side="left") 
    
    
    
    self.qta.focus()
    
    tk.Label(
            self.quadro,
            text="Desconto Reais",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left")
    
    text_desc = tk.DoubleVar()    
    self.desc =tk.Entry(self.quadro, width=6, textvariable=text_desc, validate="key", validatecommand=(vcmd,  "%P"))
    self.desc.pack(side="left",padx=10)
    self.desc.bind("<KeyRelease>", self.calc)
    tk.Label(
            self.quadro,
            text="Valor Total",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left")
    
    self.text_valor_total = tk.DoubleVar()
    
    self.valorTotal =tk.Entry(self.quadro, width=8, textvariable=self.text_valor_total, validate="key", validatecommand=(vcmd,  "%P"))
    self.valorTotal.pack(side="left",padx=10)
    
    
            
    
    tk.Button(
    self.quadro,
    text=("Adicionar Forma Pagamento"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.forma_pagamento(self.valorTotal.get())).pack(side="left")
    
    tk.Button(
        self.quadro,
        text=("Finalizar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5, 
        
        command=lambda: self.criar_atendimento()).pack(side="left")
    
    
    quandro2 = tk.LabelFrame(self, text = "Pesquisar Clientes",  background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
    quandro2.configure(height=1)
    quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

        
    self.pNome =tk.Entry(quandro2)
    self.pNome.bind('<Return>',(lambda event: self.pesquisaCliente()))
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
    
    command=lambda: self.pesquisaCliente()).pack(side="left",padx=10)
    
    

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
    
    
    self.focus_force()
    self.grab_set()


  def popular(self):
    self.tv.delete(*self.tv.get_children())
    cliente = dados.db_listar_cliente()

    for c in cliente:
        self.tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))


  def limitar_tamanho(self,P):
    if P == "": return True
    try:
        value = float(P)
    except ValueError:
        return False
    return 0 <= value <= 10000
  
  def calc(self,e):
    b = float(self.desc.get())
    soma = 0
    for i in self.options:
        soma += int(i[0]) * float(i[2])
    a = soma - b
    self.text_valor_total.set(a)


  def pesquisaCliente(self):
    self.tv.delete(*self.tv.get_children())
    historico = dados.db_historico_cliente(self.pNome.get())
    self.pNome.delete(0,tk.END)
    for c in historico:
        self.tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))


  def adicionarServico(self):
    if self.qta.get() == "" or self.textArea.get() == "" or self.valor.get() == "0.0":
        showinfo("ERRO", "Digite Todos os Dados", parent=self)
        return
    items =[self.qta.get(),self.textArea.get(), self.valor.get()]
    self.options.append(items)
    total = int(self.qta.get()) * float(self.valor.get())
    self.tv2.insert("","end", values=(self.qta.get(),self.textArea.get(), self.valor.get(), total))
    self.colTotal()
    self.qta.delete(0,tk.END)
    self.textArea.delete(0,tk.END)
    self.lb_valor.set(0.0)
    self.qta.focus()


  def colTotal(self):
    soma = 0
    for i in self.options:
        soma += int(i[0]) * float(i[2])
    self.text_valor_total.set(soma)


  def deletar(self):
    try:
        itemSelecionado = self.tv2.selection()[0]
        valores = self.tv2.item(itemSelecionado, "value")
        for i in range(len(self.options)):
            if self.options[i][1] == valores[1]:
                self.options.pop(i)
                
                self.colTotal()
        self.tv2.delete(itemSelecionado)
        
    except:
        showinfo("ERRO","Selecione o item a ser deletado", parent=self)

  def forma_pagamento(self, valor):
    Forma_Pagamento(self.master, valor, self.on_toplevel2_close)


  def on_toplevel2_close(self, data):
    self.formaPag = data
    
    
    

  def criar_atendimento(self):
    try:
        descricoItem = ""
        for j in self.options:
            descricoItem += "Quan. {},{}, V. unitario: {}\n".format(j[0], j[1], j[2])
        for i in self.formaPag:
            descricoItem += "Valor-{}, Pagamento-{}\n".format(i[0], i[1])

        # Verifique se um item está selecionado
        if not self.tv.selection():
            showerror("ERRO!", "Precisa Selecionar um Cliente", parent=self)
            return

        items = self.tv.selection()[0]
        id = self.tv.item(items, "value")

        desconto = self.desc.get()
        try:
            v = float(self.desc.get()) + float(self.valorTotal.get())
        except ValueError:
            showerror("ERRO!", "Valores de desconto ou total são inválidos", parent=self)
            return
        
        vt = self.valorTotal.get()

        try:
            dataR = datetime.strptime(self.data.get(), "%d/%m/%Y")
        except ValueError:
            showerror("ERRO!", "Data inválida", parent=self)
            return
        
        descricao = descricoItem
        formaPagamento = self.formaPag

        forma_pagamento_id = None
        for f in dados.db_listar_forma_pagamento():
            if f["nome"] == self.formaPag[0][1]:
                forma_pagamento_id = f["id_forma_pagamento"]
                break

        if not all([v, vt, dataR, descricao, forma_pagamento_id]):
            showerror("ERRO!", "Preencha todos os Campos", parent=self)
            return

        msg = askquestion("?", "Deseja Finalizar o Atendimento?", parent=self)

        if msg == "yes":
            dados.criar_atendimento(id[0], v, desconto, vt, forma_pagamento_id, descricao, dataR)
            showinfo(title=False, message="Atendimento Adicionado com sucesso", parent=self)
            self.after(500, self.destroy)
            
    except Exception as e:
        showerror("ERRO!", f"Um erro ocorreu: {str(e)}", parent=self)
  
  def update_preco_service(self, event):
    selected_service = self.textArea.get()
    if selected_service in self.service_map:
        selected_preco_service = self.service_map[selected_service]
        self.lb_valor.set(selected_preco_service)