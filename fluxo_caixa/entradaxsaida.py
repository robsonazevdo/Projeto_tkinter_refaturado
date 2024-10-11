import tkinter as tk
import Banco as dados  
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion
from tkcalendar import DateEntry
from datetime import datetime
import json

class Entrada_Saida(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)

    self.title("Fluxo de Caixa")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 10
    y = int(self.winfo_screenheight() * 0.03)
    self.geometry('1000x690+' + str(x) + '+' + str(y))
    self.configure(background="#b4918f")
    
    # Configuração do Frame Principal
    main_frame = tk.Frame(self, background="#b4918f")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
    
    # Frame para buscar por data
    frame_busca = tk.LabelFrame(main_frame, text="Buscar Data", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12, 'bold'))
    frame_busca.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

    self.data = DateEntry(frame_busca, selectmode='day', locale='pt_br', date_pattern='dd/MM/yyyy')
    self.data.bind('<Return>', (lambda event: self.buscarAtendimento2()))
    self.data.pack(side="left", padx=10)

    tk.Button(
        frame_busca,
        text="Buscar",
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd=5,
        command=self.buscarAtendimento2
    ).pack(side="left", padx=10)

    tk.Button(
        frame_busca,
        text="Atualizar",
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd=5,
        command=self.atualizar
    ).pack(side="left", padx=10)

    tk.Button(
        frame_busca,
        text="Registrar Saída",
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd=5,
        command=self.saida
    ).pack(side="left", padx=10)
    
    # Frame para exibir as entradas
    quadro_entradas = tk.LabelFrame(main_frame, text="Entradas", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 14))
    quadro_entradas.grid(row=1, column=0, pady=10, sticky="nswe")

    self.tv = ttk.Treeview(quadro_entradas, columns=("id", "Data", "Nome", "Valor_Pago", "forma"), show="headings")
    self.tv.column("id", minwidth=0, width=30, anchor=tk.W)
    self.tv.column("Data", minwidth=15, width=70, anchor=tk.W)
    self.tv.column("Nome", minwidth=15, width=150, anchor=tk.W)
    self.tv.column("Valor_Pago", minwidth=0, width=100, anchor=tk.W)
    self.tv.column("forma", minwidth=0, width=100, anchor=tk.W)
    self.tv.heading("id", text="ID", anchor=tk.W)
    self.tv.heading("Data", text="DATA", anchor=tk.W)
    self.tv.heading("Nome", text="NOME", anchor=tk.W)
    self.tv.heading("Valor_Pago", text="VALOR PAGO", anchor=tk.W)
    self.tv.heading("forma", text="FORMA DE PAGAMENTO", anchor=tk.W)
    self.tv.pack(fill=tk.BOTH, expand=True)

    label_total_entradas = tk.Label(quadro_entradas, text="Total de Entradas: ", fg="#696969", background="#b4918f", font=('TkMenuFont', 12, 'bold'))
    label_total_entradas.pack(side="left", padx=10)

    self.string_variable = tk.StringVar()
    total_entradas_label = tk.Label(quadro_entradas, textvariable=self.string_variable, bd=5, background="#b4918f", fg="#ADD8E6", font=('TkMenuFont', 12, 'bold'))
    total_entradas_label.pack(side="left")
    
    # Frame para exibir as saídas
    quadro_saidas = tk.LabelFrame(main_frame, text="Saídas", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 14))
    quadro_saidas.grid(row=1, column=1, padx=20, pady=10, sticky="nswe")

    self.tvs = ttk.Treeview(quadro_saidas, columns=("id", "Data", "Nome", "Valor_Pago", "forma"), show="headings")
    self.tvs.column("id", minwidth=0, width=30, anchor=tk.W)
    self.tvs.column("Data", minwidth=15, width=70, anchor=tk.W)
    self.tvs.column("Nome", minwidth=15, width=150, anchor=tk.W)
    self.tvs.column("Valor_Pago", minwidth=0, width=100, anchor=tk.W)
    self.tvs.column("forma", minwidth=0, width=100, anchor=tk.W)
    self.tvs.heading("id", text="ID", anchor=tk.W)
    self.tvs.heading("Data", text="DATA", anchor=tk.W)
    self.tvs.heading("Nome", text="DESCRIÇÃO", anchor=tk.W)
    self.tvs.heading("Valor_Pago", text="VALOR PAGO", anchor=tk.W)
    self.tvs.heading("forma", text="OBSERVAÇÃO", anchor=tk.W)
    self.tvs.pack(fill=tk.BOTH, expand=True)

    label_total_saidas = tk.Label(quadro_saidas, text="Total de Saídas: ", fg="#696969", background="#b4918f", font=('TkMenuFont', 12, 'bold'))
    label_total_saidas.pack(side="left", padx=10)

    self.string_variable1 = tk.StringVar()
    total_saidas_label = tk.Label(quadro_saidas, textvariable=self.string_variable1, bd=5, background="#b4918f", fg="#ADD8E6", font=('TkMenuFont', 12, 'bold'))
    total_saidas_label.pack(side="left")
    
    # Label para exibir o fluxo do dia
    frame_fluxo_dia = tk.Frame(main_frame, background="#b4918f")
    frame_fluxo_dia.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

    total_fluxo_dia_label = tk.Label(frame_fluxo_dia, text='Fluxo do dia:', bd=5, background="#b4918f", fg="#ADD8E6", font=('TkMenuFont', 25, 'bold'))
    total_fluxo_dia_label.pack(side="left", padx=10)

    self.subtracao = tk.StringVar()
    self.total_fluxo_dia = tk.Label(frame_fluxo_dia, textvariable=self.subtracao, bd=5, background="#b4918f", font=('TkMenuFont', 25, 'bold'))
    self.total_fluxo_dia.pack(side="left", padx=10)
    
    # Frame para exibir o fluxo total do mês
    quadro_fluxo_mes = tk.LabelFrame(main_frame, text="Fluxo Total do Mês", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 14))
    quadro_fluxo_mes.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

    tk.Label(quadro_fluxo_mes, text="Meses: ", bd=5, background="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=0, column=0)
    
    meses = ('Selecione o Mês', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
    anos = [str(year) for year in range(datetime.now().year - 10, datetime.now().year + 11)]

    mes_do_Ano = datetime.today()
    self.somaMes = tk.StringVar()
    total_saida_mes = self.switch_case(mes_do_Ano.month, mes_do_Ano.year)
    
    
    if float(total_saida_mes) < 0:
        fgcm = "#800000"
    else:  
        fgcm = "#00008B"
    
    self.somaMes.set(f"{float(total_saida_mes):.2f}")
    
    totalEntradasaida1 = tk.Label(quadro_fluxo_mes, text='Total de Saída Mês', bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
    totalEntradasaida1.grid(column=0, row=1, padx=2, pady=1, sticky='w')
    
    totalEntradas1 = tk.Label(quadro_fluxo_mes, textvariable=self.somaMes, bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
    totalEntradas1.grid(column=1, row=1, padx=20, pady=1, sticky='e')


    self.somaEntradasMes = tk.StringVar()
    self.somaEntradasMes.set(self.switch_case_entrada(mes_do_Ano.month, mes_do_Ano.year))
    
    
    totalEntradasaida2 = tk.Label(quadro_fluxo_mes, text='Total de Entradas Mês', bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
    totalEntradasaida2.grid(column=0, row=2, padx=2, pady=1, sticky='w')
    
    totalSaidas_ = tk.Label(quadro_fluxo_mes, textvariable=self.somaEntradasMes, bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
    totalSaidas_.grid(column=1, row=2, padx=20, pady=1, sticky='e') 

    
    

    self.combobox_meses = ttk.Combobox(quadro_fluxo_mes, values=meses, state='readonly')
    self.combobox_meses.grid(row=0, column=1)
    self.combobox_meses.current(datetime.today().month)

    tk.Label(quadro_fluxo_mes, text="Ano: ", background="#b4918f", fg="white", font=('TkMenuFont', 12)).grid(row=0, column=2, padx=10)
    self.combobox_ano = ttk.Combobox(quadro_fluxo_mes, values=anos, state='readonly')
    self.combobox_ano.grid(row=0, column=3)
    self.combobox_ano.current(10)

    tk.Button(
        quadro_fluxo_mes,
        text="Buscar",
        font=('TkMenuFont', 12),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd=5,
        command=self.buscarPorMes
    ).grid(row=0, column=4, padx=10)
    
    self.total_fluxo_label = tk.Label(quadro_fluxo_mes, text="", bd=5, background="#b4918f", fg="white", font=('TkMenuFont', 14, 'bold'))
    self.total_fluxo_label.grid(row=1, column=0, columnspan=5, pady=10)
    
    

    self.buscarAtendimento2()
    self.focus_force()
    self.grab_set()
    

  def buscar_por_mes_ano(self, mes_numero, ano_selecionado):
      self.tv.delete(*self.tv.get_children())
      self.tvs.delete(*self.tvs.get_children())

      

      historico = dados.trazer_entradas_mes_ano(mes_numero - 1, ano_selecionado)
      historicoConsulta = dados.trazer_soma_entrada_mes_ano(mes_numero - 1, ano_selecionado)
      todosSaida = dados.db_listar_saida_mes_ano2(mes_numero - 1, ano_selecionado)
      somaSaida = dados.db_historico_saida333(mes_numero - 1, ano_selecionado)
      
      
      if somaSaida[0]['tt'] == None:
          saida = f"{0:.2f}"
      else:
          saida = f"{somaSaida[0]['tt']:.2f}"
          
      
      if historicoConsulta[0]['tt'] == None:
          entrada = f"{0:.2f}"
      else:
          entrada = f"{historicoConsulta[0]['tt']:.2f}"
          

      self.string_variable1.set(saida)
      self.string_variable.set(entrada) 
      
      corLabel = f"{float(self.string_variable.get()) - float(self.string_variable1.get()):.2f}"
      
      if float(corLabel) < 0:
          self.total_fluxo_dia.configure(foreground="#800000")
          self.subtracao.set(corLabel)
      else:
          self.total_fluxo_dia.configure(foreground="#00008B")
          self.subtracao.set(corLabel)
      
                  
      for s in todosSaida:
          self.tvs.insert("","end", values=(s['id_saida'],s["data"],s['descricao'],"%.2f" %s['valor_total'],s['observacao'])) 
      
      for c in historico:
        forma_pagamento_dict = json.loads(c['forma_pagamento'])
        # Obter a primeira chave (forma de pagamento)
        primeira_parte = list(forma_pagamento_dict.keys())[0]
        self.tv.insert("","end", values=(c['numero_comanda'],c["data_venda"],c['nome'],"%.2f" %c['valor_total'],primeira_parte))

      d = self.data.get().split("/")
      res = [ele.lstrip('0') for ele in d] 
      
      
      total_saida_mes = self.switch_case(int(res[1]), int(self.data.get()[6:]))
      LabelEntradaMes = float(self.switch_case_entrada(int(res[1]), int(self.data.get()[6:])))

      
      ts = float(total_saida_mes)
      self.somaMes.set(f"{ts:.2f}")
      self.somaEntradasMes.set(f"{LabelEntradaMes:.2f}")

  def buscarAtendimento2(self):
      self.tv.delete(*self.tv.get_children())
      self.tvs.delete(*self.tvs.get_children())

      historico = dados.db_trazer_historico_atendimento(datetime.strptime(self.data.get(), "%d/%m/%Y"))
      historicoConsulta = dados.db_historico_entrada(datetime.strptime(self.data.get(), "%d/%m/%Y"))
      todosSaida = dados.db_listar_saida(datetime.strptime(self.data.get(), "%d/%m/%Y"))
      somaSaida = dados.db_historico_saida(datetime.strptime(self.data.get(), "%d/%m/%Y"))
      
      
      if somaSaida[0]['tt'] == None:
          saida = f"{0:.2f}"
      else:
          saida = f"{somaSaida[0]['tt']:.2f}"
          
      
      if historicoConsulta[0]['tt'] == None:
          entrada = f"{0:.2f}"
      else:
          entrada = f"{historicoConsulta[0]['tt']:.2f}"

      self.string_variable1.set(saida)
      self.string_variable.set(entrada) 
      
      corLabel = f"{float(self.string_variable.get()) - float(self.string_variable1.get()):.2f}"
      
      if float(corLabel) < 0:
          self.total_fluxo_dia.configure(foreground="#800000")
          self.subtracao.set(corLabel)
      else:
          self.total_fluxo_dia.configure(foreground="#00008B")
          self.subtracao.set(corLabel)
      
                  
      for s in todosSaida:
          self.tvs.insert("","end", values=(s['id_saida'],s["data"],s['descricao'],"%.2f" %s['valor_total'],s['observacao'])) 
      
      for c in historico:
        forma_pagamento_dict = json.loads(c['forma_pagamento'])
       
        primeira_parte = list(forma_pagamento_dict.keys())[0]
        self.tv.insert("","end", values=(c['numero_comanda'],c["data_venda"],c['nome'],"%.2f" %c['valor_total'],primeira_parte))
        

      d = self.data.get().split("/")
      res = [ele.lstrip('0') for ele in d] 
      self.combobox_meses.current(int(res[1]))
      
      
      
      total_saida_mes = self.switch_case(int(res[1]), int(self.data.get()[6:]))
      LabelEntradaMes = float(self.switch_case_entrada(int(res[1]), int(self.data.get()[6:])))

      
      ts = float(total_saida_mes)
      self.somaMes.set(f"{ts:.2f}")
      self.somaEntradasMes.set(f"{LabelEntradaMes:.2f}")


  def atualizar(self):
    self.tv.delete(*self.tv.get_children())
    self.tvs.delete(*self.tvs.get_children())
      

  def saida(self):
      from fluxo_caixa.saida import Saida
      Saida(self)

  def switch_case(self, mes,y):
      if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
          soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 31))
          return float(soma[0]['tt']) * -1 if soma[0]['tt'] != None else f"{0:.2f}"
      
      elif mes == 2:
          if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
              soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 29))
              return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
          else:
              soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 28))
              return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
          
      else:
          soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 30))
          return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"          


  def switch_case_entrada(self,mes,y):
      if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
          soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 31))
          return float(soma[0]['tt']) if soma[0]['tt'] != None else f"{0:.2f}"
      
      elif mes == 2:
          if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
              soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 29))
              return float(f"{soma[0]['tt']:.2f}") if soma[0]['tt'] != None else float(f"{0:.2f}")
          else:
              soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 28))
              return float(f"{soma[0]['tt']:.2f}") if soma[0]['tt'] != None else float(f"{0:.2f}")
          
      else:
          soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 30))
          return float(f"{soma[0]['tt']:.2f}") if soma[0]['tt'] != None else float(f"{0:.2f}")
        
  def buscarPorMes(self):
    mes_selecionado = self.combobox_meses.get()
    ano_selecionado = self.combobox_ano.get()
    if mes_selecionado and ano_selecionado:
        mes_numero = self.combobox_meses.current() + 1
        self.buscar_por_mes_ano(mes_numero, ano_selecionado)

