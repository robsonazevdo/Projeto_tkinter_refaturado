import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, showwarning, askyesno
# from maskedentry import*
from tkcalendar import DateEntry
from datetime import datetime, date
import json
# import calendario


class BeautySalon(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)

    self.title("Comanda")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 4
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('800x600+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")

    # Dicionário para armazenar comandas e seus serviços
    self.comandas = {}
    vcmd = self.register(func=self.limitar_tamanho)

    # Frame para número da comanda, nome do cliente e funcionário
    self.frame_comanda = tk.Frame(self, background="#b4918f")
    self.frame_comanda.pack(pady=10)

    tk.Label(self.frame_comanda, text="Número da Comanda:", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).grid(row=0, column=0, padx=5)
    self.entry_comanda = tk.Entry(self.frame_comanda)
    self.entry_comanda.grid(row=0, column=1, padx=5)


    client = dados.db_listar_cliente()
    self.client_map = {c['nome']: c['id_cliente'] for c in client}
    self.client_names = list(self.client_map.keys())

    tk.Label(self.frame_comanda, text="Nome do Cliente:", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).grid(row=1, column=0, padx=5)
    self.entry_cliente = ttk.Combobox(self.frame_comanda, values=self.client_names)
    self.entry_cliente.grid(row=1, column=1, padx=5)

    self.entry_cliente.bind('<KeyRelease>', self.pesquisar_cliente)


    funcionario = dados.db_listar_funcionarios()
    self.funcionario_map = {fun['nome']: fun['id_funcionario'] for fun in funcionario}
    funcionario_names = list(self.funcionario_map.keys())

    tk.Label(self.frame_comanda, text="Funcionário Responsável:", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).grid(row=2, column=0, padx=5)
    self.entry_funcionario = ttk.Combobox(self.frame_comanda, values=funcionario_names)
    self.entry_funcionario.grid(row=2, column=1, padx=5)


    operacao = dados.db_listar_operacao()
    self.operacao_map = {op['nome']: op['id_operacao'] for op in operacao}
    operacao_names = list(self.operacao_map.keys())

    tk.Label(self.frame_comanda, text="Operação", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).grid(row=3, column=0, padx=5)
    self.entry_operacao = ttk.Combobox(self.frame_comanda, values=operacao_names)
    self.entry_operacao.grid(row=3, column=1, padx=5)

    tk.Button(self.frame_comanda, text="Nova Comanda", font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,command=self.nova_comanda).grid(row=0, column=3, rowspan=3, padx=5)

    self.data = DateEntry(self.frame_comanda, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
    self.data.grid(row=0, column=2, rowspan=3, padx=5)

    



    # Frame para adicionar serviços
    self.frame_servico = tk.Frame(self, background="#b4918f")
    self.frame_servico.pack(pady=10)


    service = dados.db_listar_servico()
    self.service_map = {serv['nome_servico']: serv['preco_servico'] for serv in service}
    service_names = list(self.service_map.keys())


    tk.Label(self.frame_servico, text="Serviço:", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).grid(row=0, column=0, padx=5)
    self.entry_servico = ttk.Combobox(self.frame_servico, values=service_names)
    self.entry_servico.bind("<<ComboboxSelected>>", self.update_preco_service)
    self.entry_servico.grid(row=0, column=1, padx=5)


    tk.Label(self.frame_servico, text="Quantidade:", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).grid(row=1, column=0, padx=5)
    vcmd_int = self.register(self.validar_inteiros)
    self.entry_quantidade = tk.Entry(self.frame_servico, validate="key", validatecommand=(vcmd_int, '%P'))
    self.entry_quantidade.insert(0, "1")
    self.entry_quantidade.grid(row=1, column=1, padx=5, sticky="e")
    

    tk.Label(self.frame_servico, text="Preço (R$):", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).grid(row=2, column=0, padx=5)
    self.lb_valor = tk.DoubleVar()
    self.entry_preco = tk.Entry(self.frame_servico, textvariable=self.lb_valor, validate="key", validatecommand=(vcmd, "%P"), width=12)
    self.entry_preco.grid(row=2, column=1, padx=5, sticky="e")



    tk.Button(self.frame_servico, text="Adicionar Serviço", font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, command=self.adicionar_servico).grid(row=4, column=0, pady=10)


    # Botão para remover serviço
    tk.Button(self.frame_servico, text="Remover Serviço", font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, command=self.remover_servico).grid(row=4, column=1, pady=10)

    tk.Label(self, text="Desconto:", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12)).pack(padx=5, pady=5, side='left')
    vcmd_float = self.register(self.validar_float)

    self.lb_desconto = tk.DoubleVar()
    self.entry_desconto = tk.Entry(self, width=8, font=('TkMenuFont', 12), bd=5, textvariable=self.lb_desconto, validate="key", validatecommand=(vcmd_float, '%P'))
    self.entry_desconto.pack(padx=15, pady=15, side='left')

    self.lb_desconto.set("0.00")

    self.entry_desconto.bind('<KeyRelease>', self.calcular_total_com_desconto)


    # Label para mostrar o total da comanda
    self.label_total = tk.Label(
    self, 
    text="Total: R$ 0.00", 
    font=("Helvetica", 14), 
    background="#b4918f", 
    highlightbackground="white",  
    highlightthickness=4,
    padx=20, 
    pady=10   
)
    self.label_total.pack(padx=30, pady=20, side='left')

    # Lista para mostrar os serviços adicionados
    self.listbox_servicos = tk.Listbox(self, width=50)
    self.listbox_servicos.pack(padx=30, pady=20)

    # Botão para finalizar a comanda
    self.button_finalizar = tk.Button(self, text="Finalizar Comanda", font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5, command=self.finalizar_comanda)
    self.button_finalizar.pack(pady=10)


  def nova_comanda(self):
    comanda_numero = self.entry_comanda.get()
    data = datetime.strptime(self.data.get(), "%d/%m/%Y")

    cliente = self.entry_cliente.get()
    if cliente in self.client_map:
        selected_id_ = self.client_map[cliente]
        
    funcionario = self.entry_funcionario.get()
    if funcionario in self.funcionario_map:
        selected_id_funcionario = self.funcionario_map[funcionario]

    operacao = self.entry_operacao.get()
    if operacao in self.operacao_map:
        selected_id_operacao = self.operacao_map[operacao]
    
    
    if comanda_numero and cliente and funcionario:
        ja_existia, self.nova_comanda = dados.criar_comanda(selected_id_, comanda_numero, data, selected_id_operacao, 1, selected_id_funcionario)
        if ja_existia:
            showwarning("Comanda Existente", "Essa comanda já existe!",parent=self)
        else:
            # Armazenar a comanda com informações do cliente, funcionário e serviços
            self.comandas[comanda_numero] = {'cliente': cliente, 'funcionario': funcionario, 'servicos': [], 'pagamento': None}
            self.listbox_servicos.delete(0, tk.END)
            self.label_total.config(text="Total: R$ 0.00")
            showinfo("Nova Comanda", f"Comanda {comanda_numero} criada para o cliente {cliente}!",parent=self)
    else:
        showerror("Erro", "Preencha todos os campos para criar a comanda!", parent=self)


  def adicionar_servico(self):
    comanda_numero = self.entry_comanda.get()
    
    # Verifica se a comanda existe e está aberta
    if not dados.verificar_comanda_aberta(comanda_numero):
        showwarning("Comanda Fechada", "Não é possível adicionar itens a uma comanda fechada!", parent=self)
        return

    servico = self.entry_servico.get()
    quantidade = self.entry_quantidade.get()
    preco = self.entry_preco.get()

    if self.comandas == {}:
        self.comandas[comanda_numero] = {'cliente': self.entry_cliente.get(), 'funcionario': self.entry_funcionario.get(), 'servicos': [], 'pagamento': None}
        self.listbox_servicos.delete(0, tk.END)
        self.label_total.config(text="Total: R$ 0.00")

    if comanda_numero and comanda_numero in self.comandas:
        try:
            preco = float(preco)
            quantidade = int(quantidade)
            total_preco_servico = preco * quantidade

            # Adiciona o serviço à lista de serviços da comanda
            self.comandas[comanda_numero]['servicos'].append((servico, quantidade, total_preco_servico))
            
            # Exibe o serviço adicionado na listbox
            self.listbox_servicos.insert(tk.END, f"{servico} (x{quantidade}) - R$ {total_preco_servico:.2f}")
            
            # Atualiza o total da comanda
            self.atualizar_total(comanda_numero)
        except ValueError:
            showerror("Erro", "Preço ou quantidade inválidos!", parent=self)
    else:
        showwarning("Erro", "Comanda inválida ou não existente!", parent=self)


  def atualizar_total(self, comanda_numero):
    
    
    total = sum(total_preco for _, _,  total_preco in self.comandas[comanda_numero]['servicos'])
    self.label_total.config(text=f"Total: R$ {total:.2f}")
    self.total_sem_desconto = total
    self.total_ = total


  def calcular_total_com_desconto(self, event):
    desconto = self.entry_desconto.get()
    if desconto:
        try:
            desconto = float(desconto)
        except ValueError:
            showwarning("Erro", "Desconto inválido!", parent=self)
            desconto = 0.0
    else:
        desconto = 0.0

    
    total = self.total_sem_desconto
    total_com_desconto = total - desconto
    self.label_total.config(text=f"Total: R$ {total_com_desconto:.2f}")
    self.total_ = total_com_desconto 


  def finalizar_comanda(self):
    comanda_numero = self.entry_comanda.get()

    
    if not comanda_numero or comanda_numero not in self.comandas:
        showwarning("Erro", "Nenhuma comanda válida foi criada!", parent=self)
        return

    
    if not self.comandas[comanda_numero]['servicos']:
        showwarning("Erro", "Nenhum serviço foi adicionado à comanda!", parent=self)
        return

    
    confirmar = askyesno("Finalizar Comanda", f"Tem certeza que deseja finalizar a comanda {comanda_numero}?", parent=self)

    if confirmar:
        for index in range(self.listbox_servicos.size()):
            item = self.listbox_servicos.get(index)
            item_parts = extrair_dados(item)
            
            
            #nome_servico, q, t, r, preco = item.split(' ')
            nome_servico = item_parts[0]
            q = item_parts[1]
            id_servico = dados.obter_id_servico(nome_servico)
            id_funcionario = dados.obter_id_funcionario(self.entry_funcionario.get())
            id_comanda = dados.obter_id_comanda(comanda_numero)
            
            if id_servico and id_funcionario:
                #dados.criar_additems(id_comanda, id_servico, q, id_funcionario)
                print(id_comanda, id_servico, q, id_funcionario)
            else:
                showerror("Erro: Não foi possível encontrar o ID do serviço ou do funcionário.")

        if comanda_numero in self.comandas:
            self.abrir_tela_pagamento(comanda_numero)
        else:
            showwarning("Erro", "Comanda inválida ou não existente!",parent=self)
    else:
        showinfo("Operação Cancelada", f"A comanda {comanda_numero} não foi finalizada.", parent=self)
        

  def abrir_tela_pagamento(self, comanda_numero):
    # Criar nova janela para escolher a forma de pagamento
    pagamento_window = tk.Toplevel(self)
    pagamento_window.title(f"Pagamento - Comanda {comanda_numero}")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x =  pagamento_window.winfo_screenwidth() // 4
    y = int(self.winfo_screenheight() * 0.1)
    pagamento_window.geometry('700x600+' + str(x) + '+' + str(y))
    pagamento_window.configure(background="#b4918f")

    # Total da comanda
    total_comanda = self.total_  
    self.valor_restante = tk.DoubleVar(value=total_comanda)

    tk.Label(pagamento_window, text=f"Escolha a forma de pagamento para a Comanda {comanda_numero}. Total: R$ {total_comanda:.2f}", font=("Helvetica", 12), background="#b4918f").pack(pady=10)

    # Label para mostrar o valor restante
    self.label_valor_restante = tk.Label(pagamento_window, text=f"Valor Restante: R$ {total_comanda:.2f}", font=("Helvetica", 12), background="#b4918f", fg="red")
    self.label_valor_restante.pack(pady=10)

    # Frame para conter as opções de pagamento e entradas
    frame_pagamento = tk.Frame(pagamento_window, background="#b4918f")
    frame_pagamento.pack(pady=10)

    # Dicionário para armazenar o valor de cada forma de pagamento
    self.pagamento_valores = {}


    for forma in dados.db_listar_forma_pagamento():
        row = tk.Frame(frame_pagamento, background="#b4918f")
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Label para a forma de pagamento
        tk.Label(row, text=forma['nome'], background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12), width=15).pack(side=tk.LEFT)

        # Campo de entrada para o valor
        entry_valor = tk.Entry(row, width=10)
        entry_valor.pack(side=tk.LEFT)

        # Armazenar o campo de entrada no dicionário
        self.pagamento_valores[forma['nome']] = entry_valor

        # Adicionar evento de verificação quando o valor mudar
        entry_valor.bind("<KeyRelease>", self.atualizar_valor_restante)


    # Botão para finalizar o pagamento e chamar a tela de atendimento
    tk.Button(pagamento_window, text="Confirmar Pagamento", font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,command=lambda: self.finalizar_atendimento(pagamento_window, self.entry_comanda.get())).pack(pady=10)


  def atualizar_valor_restante(self,event):
    total_pago = 0.0

    # Somar os valores de todas as formas de pagamento
    for forma, entry in self.pagamento_valores.items():
        valor = entry.get()
        if valor:
            try:
                total_pago += float(valor)
            except ValueError:
                pass  # Ignora se o valor não for um número

    # Atualizar o valor restante
    valor_restante = self.total_ - total_pago
    self.valor_restante.set(valor_restante)

    # Atualizar o label que exibe o valor restante
    self.label_valor_restante.config(text=f"Valor Restante: R$ {valor_restante:.2f}")

    # Verifique se o valor restante é zero ou negativo e altere a cor do texto
    if valor_restante <= 0:
        self.label_valor_restante.config(fg="green")
    else:
        self.label_valor_restante.config(fg="red")


  def finalizar_atendimento(self, pagamento_window, comanda_numero):
    pagamentos = {}
    total_pago = 0.0

    # Obter os valores inseridos para cada forma de pagamento
    for forma, entry in self.pagamento_valores.items():
        valor = entry.get()
        if valor:  # Verifica se um valor foi inserido
            try:
                valor_float = float(valor)
                pagamentos[forma] = valor_float
                total_pago += valor_float
            except ValueError:
                showerror("Erro", f"Valor inválido para {forma}. Insira um número.", parent=self)
                return

    # Exibir o total e as formas de pagamento escolhidas
    showinfo("Pagamento Confirmado", f"Total pago: R$ {total_pago:.2f}\nFormas de pagamento: {pagamentos} \nDesconto: {self.entry_desconto.get()}", parent=self)

    # Fechar a janela de pagamento
    pagamento_window.destroy()
    self.abrir_tela_atendimento(comanda_numero, pagamentos)


  def abrir_tela_atendimento(self, comanda_numero, pagamentos):      
        # Criar nova janela para exibir o atendimento
        atendimento_window = tk.Toplevel(self)
        atendimento_window.title(f"Atendimento - Comanda {comanda_numero}")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x =  atendimento_window.winfo_screenwidth() // 4
        y = int(self.winfo_screenheight() * 0.1)
        atendimento_window.geometry('700x600+' + str(x) + '+' + str(y))
        atendimento_window.configure(background="#b4918f")


        # Dados do cliente e funcionário
        cliente = self.comandas[comanda_numero]['cliente']
        funcionario = self.comandas[comanda_numero]['funcionario']
        pagamento = pagamentos

        # Exibir dados do cliente, funcionário e forma de pagamento
        tk.Label(atendimento_window, text=f"Comanda {comanda_numero}", font=("Helvetica", 14), background="#b4918f").pack(pady=10)
        tk.Label(atendimento_window, text=f"Cliente: {cliente}", font=("Helvetica", 12), background="#b4918f").pack(pady=5)
        tk.Label(atendimento_window, text=f"Funcionário: {funcionario}", font=("Helvetica", 12), background="#b4918f").pack(pady=5)
        tk.Label(atendimento_window, text=f"Forma de Pagamento: {pagamento}", font=("Helvetica", 12), background="#b4918f").pack(pady=5)
        tk.Label(atendimento_window, text=f"Desconto: {self.entry_desconto.get()}", font=("Helvetica", 12), background="#b4918f").pack(pady=5)
        
        total = self.total_
        
        # Mostrar os serviços da comanda
        listbox_atendimento = tk.Listbox(atendimento_window, width=50)
        listbox_atendimento.pack(pady=10)

      
        
        # Adicionar serviços na listbox de atendimento
        for servico, quantidade, total_preco_servico in self.comandas[comanda_numero]['servicos']:
            listbox_atendimento.insert(tk.END, f"{servico} (x{quantidade}) - R$ {total_preco_servico:.2f}")


        # Mostrar total
        tk.Label(atendimento_window, text=f"Total: R$ {total:.2f}", font=("Helvetica", 14)).pack(pady=10)

        # Botão de finalizar atendimento
        tk.Button(atendimento_window, text="Finalizar Atendimento", command=lambda: self.finalizar_atendimento_tela(atendimento_window, comanda_numero, pagamento)).pack(pady=10)


  def finalizar_atendimento_tela(self, window, comanda_numero, pagamento):
        showinfo("Atendimento Finalizado", f"Comanda {comanda_numero} foi finalizada!", parent=self)
        forma = json.dumps(pagamento)
        total = self.total_
        id_comanda = dados.obter_id_comanda(comanda_numero)
        #dados.criar_comanda_fechada(id_comanda, forma, self.entry_desconto.get(), total)
        print(id_comanda, forma, self.entry_desconto.get(), total)
        #dados.db_atualizar_comanda(2, comanda_numero)

        window.destroy()  # Fechar a janela de atendimento
        self.entry_comanda.delete(0, tk.END)  # Limpar entrada de comanda
        self.listbox_servicos.delete(0, tk.END)  # Limpar a listbox de serviços
        self.label_total.config(text="Total: R$ 0.00")  # Resetar o total


  def update_preco_service(self, event):
    selected_service = self.entry_servico.get()
    if selected_service in self.service_map:
        selected_preco_service = self.service_map[selected_service]
        self.lb_valor.set(f"{selected_preco_service:.2f}")


  def limitar_tamanho(self,P):
    if P == "": return True
    try:
        value = float(P)
    except ValueError:
        return False
    return 0 <= value <= 10000
  

  def pesquisar_cliente(self, event):
    # Obtém o texto digitado pelo usuário
    typed_text = self.entry_cliente.get()

    # Filtra a lista de clientes com base no que foi digitado
    if typed_text == '':
        self.entry_cliente['values'] = self.client_names
    else:
        filtered_names = [name for name in self.client_names if typed_text.lower() in name.lower()]
        self.entry_cliente['values'] = filtered_names

    # Abre o dropdown do Combobox para exibir as opções filtradas
    self.entry_cliente.event_generate('<Down>')


  def remover_servico(self):
    comanda_numero = self.entry_comanda.get()
    if comanda_numero in self.comandas:
        # Verifica qual item está selecionado
        selecionado = self.listbox_servicos.curselection()

        if selecionado:
            # Remove o item da listbox
            self.listbox_servicos.delete(selecionado)

            # Remove o serviço correspondente da lista de serviços da comanda
            indice = selecionado[0]
            self.comandas[comanda_numero]['servicos'].pop(indice)

            # Atualiza o total da comanda
            self.atualizar_total(comanda_numero)
        else:
            showwarning("Erro", "Selecione um serviço para remover!", parent=self)
    else:
        showwarning("Erro", "Comanda inválida ou não existente!", parent=self)
  

  def validar_inteiros(self, P):
    if P.isdigit() or P == "":
        return True
    return False
  

  def validar_float(self, P):
    if P == "" or P.replace(".", "", 1).isdigit():
        return True
    return False




import re

def extrair_dados(item):
    # Padrão para: "Escova (x1) - R$ 40.00"
    padrao = r'(\w+(?:\s\w+)*)\s+\(x(\d+)\)\s+-\s+R\$\s*([\d\.]+)'
    
    # Usa re.search para encontrar correspondências
    match = re.search(padrao, item)
    
    if match:
        nome_servico = match.group(1)  # Nome do serviço
        quantidade = int(match.group(2))  # Quantidade dentro de (x1)
        preco = float(match.group(3))  # Preço em formato decimal
        
        return nome_servico, quantidade, preco
    else:
        # Caso a string não corresponda ao formato esperado
        raise ValueError("Formato de item inválido!")




