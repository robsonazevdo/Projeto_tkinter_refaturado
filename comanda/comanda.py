import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, showwarning

# from maskedentry import*
from tkcalendar import DateEntry
from operator import neg
# import calendario


class BeautySalon(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)
    self.title("Sistema de Comanda - Salão de Beleza")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 4
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('700x500+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")

    # Dicionário para armazenar comandas e seus serviços
    self.comandas = {}

    # Frame para número da comanda, nome do cliente e funcionário
    self.frame_comanda = tk.Frame(self)
    self.frame_comanda.pack(pady=10)

    tk.Label(self.frame_comanda, text="Número da Comanda:").grid(row=0, column=0, padx=5)
    self.entry_comanda = tk.Entry(self.frame_comanda)
    self.entry_comanda.grid(row=0, column=1, padx=5)

    tk.Label(self.frame_comanda, text="Nome do Cliente:").grid(row=1, column=0, padx=5)
    self.entry_cliente = tk.Entry(self.frame_comanda)
    self.entry_cliente.grid(row=1, column=1, padx=5)

    tk.Label(self.frame_comanda, text="Funcionário Responsável:").grid(row=2, column=0, padx=5)
    self.entry_funcionario = tk.Entry(self.frame_comanda)
    self.entry_funcionario.grid(row=2, column=1, padx=5)

    tk.Button(self.frame_comanda, text="Nova Comanda", command=self.nova_comanda).grid(row=0, column=2, rowspan=3, padx=5)

    # Frame para adicionar serviços
    self.frame_servico = tk.Frame(self)
    self.frame_servico.pack(pady=10)

    tk.Label(self.frame_servico, text="Serviço:").grid(row=0, column=0, padx=5)
    self.entry_servico = tk.Entry(self.frame_servico)
    self.entry_servico.grid(row=0, column=1, padx=5)

    tk.Label(self.frame_servico, text="Preço (R$):").grid(row=1, column=0, padx=5)
    self.entry_preco = tk.Entry(self.frame_servico)
    self.entry_preco.grid(row=1, column=1, padx=5)

    tk.Button(self.frame_servico, text="Adicionar Serviço", command=self.adicionar_servico).grid(row=2, column=0, columnspan=2, pady=10)

    # Label para mostrar o total da comanda
    self.label_total = tk.Label(self, text="Total: R$ 0.00", font=("Helvetica", 14))
    self.label_total.pack(pady=10)

    # Lista para mostrar os serviços adicionados
    self.listbox_servicos = tk.Listbox(self, width=50)
    self.listbox_servicos.pack(pady=10)

    # Botão para finalizar a comanda
    self.button_finalizar = tk.Button(self, text="Finalizar Comanda", command=self.finalizar_comanda)
    self.button_finalizar.pack(pady=10)

  def nova_comanda(self):
        comanda_numero = self.entry_comanda.get()
        cliente = self.entry_cliente.get()
        funcionario = self.entry_funcionario.get()

        if comanda_numero and cliente and funcionario:
            if comanda_numero in self.comandas:
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
        servico = self.entry_servico.get()
        preco = self.entry_preco.get()

        if comanda_numero and comanda_numero in self.comandas:
            try:
                preco = float(preco)
                self.comandas[comanda_numero]['servicos'].append((servico, preco))
                self.listbox_servicos.insert(tk.END, f"{servico} - R$ {preco:.2f}")
                self.atualizar_total(comanda_numero)
            except ValueError:
                showerror("Erro", "Preço inválido!", parent=self)
        else:
            showwarning("Erro", "Comanda inválida ou não existente!", parent=self)

  def atualizar_total(self, comanda_numero):
        total = sum(preco for _, preco in self.comandas[comanda_numero]['servicos'])
        self.label_total.config(text=f"Total: R$ {total:.2f}")

  def finalizar_comanda(self):
        comanda_numero = self.entry_comanda.get()
        if comanda_numero in self.comandas:
            self.abrir_tela_pagamento(comanda_numero)
        else:
            showwarning("Erro", "Comanda inválida ou não existente!",parent=self)

  def abrir_tela_pagamento(self, comanda_numero):
    # Criar nova janela para escolher a forma de pagamento
    pagamento_window = tk.Toplevel(self)
    pagamento_window.title(f"Pagamento - Comanda {comanda_numero}")

    tk.Label(pagamento_window, text=f"Escolha a forma de pagamento para a Comanda {comanda_numero}:", font=("Helvetica", 12)).pack(pady=10)

    # Frame para conter as opções de pagamento e entradas
    frame_pagamento = tk.Frame(pagamento_window)
    frame_pagamento.pack(pady=10)

    # Dicionário para armazenar o valor de cada forma de pagamento
    self.pagamento_valores = {}

    formas_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix", "Vale-presente"]

    for forma in formas_pagamento:
        row = tk.Frame(frame_pagamento)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Label para a forma de pagamento
        tk.Label(row, text=forma, width=15).pack(side=tk.LEFT)

        # Campo de entrada para o valor
        entry_valor = tk.Entry(row, width=10)
        entry_valor.pack(side=tk.LEFT)

        # Armazenar o campo de entrada no dicionário
        self.pagamento_valores[forma] = entry_valor

    # Botão para finalizar o pagamento e chamar a tela de atendimento
    tk.Button(pagamento_window, text="Confirmar Pagamento", command=lambda: self.finalizar_atendimento(pagamento_window, comanda_numero)).pack(pady=10)


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
    showinfo("Pagamento Confirmado", f"Total pago: R$ {total_pago:.2f}\nFormas de pagamento: {pagamentos}", parent=self)

    # Fechar a janela de pagamento
    pagamento_window.destroy()
    self.abrir_tela_atendimento(comanda_numero, pagamentos)



  def abrir_tela_atendimento(self, comanda_numero, pagamentos):      
        # Criar nova janela para exibir o atendimento
        atendimento_window = tk.Toplevel(self)
        atendimento_window.title(f"Atendimento - Comanda {comanda_numero}")

        # Dados do cliente e funcionário
        cliente = self.comandas[comanda_numero]['cliente']
        funcionario = self.comandas[comanda_numero]['funcionario']
        pagamento = pagamentos

        # Exibir dados do cliente, funcionário e forma de pagamento
        tk.Label(atendimento_window, text=f"Comanda {comanda_numero}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(atendimento_window, text=f"Cliente: {cliente}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(atendimento_window, text=f"Funcionário: {funcionario}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(atendimento_window, text=f"Forma de Pagamento: {pagamento}", font=("Helvetica", 12)).pack(pady=5)

        # Mostrar os serviços da comanda
        listbox_atendimento = tk.Listbox(atendimento_window, width=50)
        listbox_atendimento.pack(pady=10)

        # Adicionar serviços na listbox
        total = 0
        for servico, preco in self.comandas[comanda_numero]['servicos']:
            listbox_atendimento.insert(tk.END, f"{servico} - R$ {preco:.2f}")
            total += preco

        # Mostrar total
        tk.Label(atendimento_window, text=f"Total: R$ {total:.2f}", font=("Helvetica", 14)).pack(pady=10)

        # Botão de finalizar atendimento
        tk.Button(atendimento_window, text="Finalizar Atendimento", command=lambda: self.finalizar_atendimento_tela(atendimento_window, comanda_numero)).pack(pady=10)

  def finalizar_atendimento_tela(self, window, comanda_numero):
        showinfo("Atendimento Finalizado", f"Comanda {comanda_numero} foi finalizada!", parent=self)
        window.destroy()  # Fechar a janela de atendimento
        self.entry_comanda.delete(0, tk.END)  # Limpar entrada de comanda
        self.listbox_servicos.delete(0, tk.END)  # Limpar a listbox de serviços
        self.label_total.config(text="Total: R$ 0.00")  # Resetar o total