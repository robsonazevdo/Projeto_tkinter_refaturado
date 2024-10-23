import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion
from tkcalendar import DateEntry
from datetime import datetime, date
import json

class Editar_Historico(tk.Toplevel):
  def __init__(self, parent, edicao_position, nome, id_comanda):
    super().__init__(parent)


    self.edicao_position = edicao_position
    self.cliente = nome
    self.id_comanda = id_comanda

    data_obj = datetime.strptime(self.edicao_position[1], "%d/%m/%Y")
    data_venda = data_obj.strftime("%Y-%m-%d %H:%M:%S")

    dic ={}
    t = dados.obter_historico_atendimento_nome_data(nome, data_venda )
    for i in t:
       
       dic[i['nome_servico']] = i['quantidade']
       
    

    json_string = self.edicao_position[4]

        # Converter a string para um dicionário
    self.dicionario = json.loads(json_string)
    
            
    self.title("Alterar Atendimento")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 8
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('1000x600+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")
    
    quadroNome = tk.LabelFrame(self, text = "Dados do Cadastro", background="#b4918f",foreground="white",bd=5, font=('TkMenuFont', 12))
    quadroNome.pack(fill="both", expand='yes',padx=10, pady=10)
    

    tk.Label(
            quadroNome,
            text="ID",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=15)
    
    lb_id = tk.StringVar()   
    self.id = tk.Entry(quadroNome, width=5, textvariable=lb_id)
    self.id.pack(side="left",padx=15)
    
    tk.Label(
            quadroNome,
            text="NOME",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=15)
    
    lb_nome = tk.StringVar()   
    c_nome = tk.Entry(quadroNome, width=50, textvariable=lb_nome)
    c_nome.pack(side="left",padx=15)
    
    cliente = dados.db_listar_cliente()
    for c in cliente:
        if c['nome'] == self.cliente:
            lb_id.set(c['id_cliente'])
            lb_nome.set(c['nome'])
            
    quadro = tk.LabelFrame(self, text = "Serviço Realizado", background="#b4918f",foreground="white", bd=5, font=('TkMenuFont', 12))
    quadro.pack(fill="both", expand='yes',padx=10, pady=10)
    
    vcmd = self.register(func=self.limitar_tamanho)
    
    tk.Label(
            quadro,
            text="Descrição",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=10)
    

    
    self.textArea = tk.Text(quadro, width=50, height=4    )
    self.textArea.pack(side="left",padx=10)

    
    self.textArea.insert(tk.END, f"{self.edicao_position[4]}, \n{dic}" )
    tk.Label(
            quadro,
            text="Data Realizada",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=10)
    
      
    self.data = DateEntry(quadro, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
    self.data.pack(side="left",padx=10)
    self.data.set_date(self.edicao_position[1])
    
    quandro1 = tk.LabelFrame(self, text = "Alterar Dados da Venda", background="#b4918f", foreground="white", bd=5, font=('TkMenuFont', 12))
    quandro1.pack(fill="both", expand='yes',padx=10, pady=10)

    

    tk.Label(
            quandro1,
            text="Valor",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=10,padx=10)
    
    lb_valor = tk.DoubleVar()   
    self.valor =tk.Entry(quandro1, width=8, textvariable=lb_valor, validate="key", validatecommand=(vcmd, "%P"))
    self.valor.pack(side="left",padx=10)
    lb_valor.set(float(self.edicao_position[2]))
    
    tk.Label(
            quandro1,
            text="Desconto Reais",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left")
    
    text_desc = tk.DoubleVar()    
    self.desc =tk.Entry(quandro1, width=6, textvariable=text_desc, validate="key", validatecommand=(vcmd,  "%P"))
    self.desc.pack(side="left",padx=10)
    self.desc.bind("<KeyRelease>", self.calc)
    text_desc.set(float(self.edicao_position[3]))
    tk.Label(
            quandro1,
            text="Valor Total",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left")
    
    text_valor_total = tk.DoubleVar()
    
    self.valorTotal =tk.Entry(quandro1, width=8, textvariable=text_valor_total, validate="key", validatecommand=(vcmd,  "%P"))
    text_valor_total.set(self.edicao_position[2])
    self.valorTotal.pack(side="left",padx=10)
    
    
    formaPagamneto = dados.db_listar_forma_pagamento()
    lista = []
    for f in formaPagamneto:
        lista.append(f['nome'])
        
    tk.Label(
            quandro1,
            text="Forma de Pagamento",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left")
    chaves = list(self.dicionario.keys())
    
    
    self.comboBox = ttk.Combobox(quandro1, values=lista, width=10)
    self.comboBox.set(chaves[0])
    self.comboBox.pack(side="left",padx=10)
    
    
    tk.Button(
    quandro1,
    text=("Salvar Altereção"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.salvar()).pack(side="left")
    
    tk.Button(
    quandro1,
    text=("Voltar"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, 
    
    command=lambda: self.voltar()).pack(side="left")
    
    
    self.focus_force()
    self.grab_set()
    
  def salvar(self):
    msg = askquestion("?","Deseja Alterar o Atendimento de {0}".format(self.edicao_position[2]), parent=self )
    if msg == "yes":
        id_forma = ""
        forma = dados.db_listar_forma_pagamento()
        for j in forma:
            if self.comboBox.get() == j["nome"]:
                id_forma = j["id_forma_pagamento"]
        
        print(self.id_comanda, self.edicao_position[0], self.id.get(),self.valor.get(), self.desc.get(), self.valorTotal.get(), id_forma, self.textArea.get("1.0",tk.END), datetime.strptime(self.data.get(), "%d/%m/%Y"))
        showinfo("Sucesso", "Atendimento foi Alterado com sucesso", parent=self)
        
        #dados.db_editar_atendimento(id_atendimento, id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao, data)
        self.destroy() 
        self.open_toplevel2()
                    
                    
  def voltar(self):
    self.open_toplevel2()
    self.destroy()  

            
  def calc(self,e):
    a = float(self.valor.get()) - float(self.desc.get())
    self.text_valor_total.set(a)
            
  def limitar_tamanho(self,P):
    if P == "": return True
    try:
        value = float(P)
    except ValueError:
        return False
    return 0 <= value <= 10000
  

  def open_toplevel2(self):
    from historico.historico import Historico_Atendimento
    Historico_Atendimento(self.master)
            
            