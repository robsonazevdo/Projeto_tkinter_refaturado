import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk, simpledialog
from tkinter.messagebox import showinfo, askyesno, askquestion, showwarning
from datetime import datetime, date
from time import strftime
from tkcalendar import DateEntry

class Atualizar_Agendamento(tk.Toplevel):
  def __init__(self, parent, items):
    super().__init__(parent)

    self.items = items

    self.title("Atualizar Agendamento")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 8
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('800x600+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")


    

    left_frame = tk.LabelFrame(self, text="Atualizar/Deletar", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')

    
    # Date picker
    self.date_label = tk.Label(left_frame, text="Data", bg='#b4918f')
    self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    self.date_entry = DateEntry(left_frame, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
    self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    self.date_inicial = self.items[2]
    
    
    if self.date_inicial:
      try:
          # Converte a string da data inicial para um objeto datetime
          date_obj = datetime.strptime(self.date_inicial, '%d/%m/%Y')
          # Define o valor inicial no DateEntry
          self.date_entry.set_date(date_obj)
      except ValueError as e:
          print(f"Erro ao configurar a data inicial: {e}")

    cliente = dados.db_listar_cliente()
    cliente_inicial = self.items[1]
   
    self.cliente_map = {cli['nome']: cli['id_cliente'] for cli in cliente}
    
    self.cliente_names = list(self.cliente_map.keys())

    self.cliente_label = tk.Label(left_frame, text="Clientes", bg='#b4918f')
    self.cliente_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    self.cliente_entry = ttk.Combobox(left_frame, values=self.cliente_names)
    self.cliente_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

   
    
    if cliente_inicial and cliente_inicial in self.cliente_map:
      self.cliente_entry.set(cliente_inicial)

      self.selected_cliente = cliente_inicial

    # Adicionar funcionalidade de pesquisa ao Combobox
    self.cliente_entry.bind("<KeyRelease>", self._on_keyrelease)
    

    service = dados.db_listar_servico()
    self.nome_servico = self.items[4]
    self.service_map = {serv['nome_servico']: serv['id_servico'] for serv in service}
    
    self.service_names = list(self.service_map.keys())
    
    # Service selection
    self.service_label = tk.Label(left_frame, text="Escolha o serviço", bg='#b4918f')
    self.service_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    self.service_entry = ttk.Combobox(left_frame, values=self.service_names)
    self.service_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    if self.nome_servico and self.nome_servico in self.service_map:
      self.service_entry.set(self.nome_servico)

      self.selected_service = self.nome_servico

    funcionario = dados.db_listar_funcionarios()
    self.nome_funcionario = self.items[5]
    # Person selection
    self.person_label = tk.Label(left_frame, text="Quem irá Realizar?", bg='#b4918f')
    self.person_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')

    # Mapping names to their respective IDs
    self.person_map = {func['nome']: func['id_funcionario'] for func in funcionario}
    
    person_names = list(self.person_map.keys())
    
    self.person_entry = ttk.Combobox(left_frame, values=person_names)
    self.person_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    if self.nome_funcionario and self.nome_funcionario in self.person_map:
      self.person_entry.set(self.nome_funcionario)

      self.selected_person = self.nome_funcionario
    
    
    
   # Label para "Escolha a hora"
    self.label = tk.Label(left_frame, text="Escolha a hora", bg='#b4918f', fg='white', font=("Helvetica", 12))
    self.label.grid(row=4, column=0, pady=5, sticky='w')

    selected_hour = self.items[3][:2]
    selected_minute = self.items[3][3:]

    # Combobox para horas
    self.hour_var = tk.StringVar()
    self.hour_combobox = ttk.Combobox(left_frame, textvariable=self.hour_var, values=[f'{i:02d}' for i in range(7,21)], state="readonly", width=3)
    self.hour_combobox.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    self.hour_combobox.set(selected_hour if selected_hour else '--')

    # Combobox para minutos
    self.minute_var = tk.StringVar()
    self.minute_combobox = ttk.Combobox(left_frame, textvariable=self.minute_var, values=[f'{i:02d}' for i in range(0,60,15)], state="readonly", width=3)
    self.minute_combobox.grid(row=4, column=1, padx=5, pady=5)
    self.minute_combobox.set(selected_minute if selected_minute else '--')

   
    self.select_button = tk.Button(left_frame, text="Selecionar", font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    command=self.update_agendamento)
    self.select_button.grid(row=6, column=0, columnspan=2, pady=10)


    


    tk.Button(
    self,
    text=("Voltar ao Ínicio"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.voltar_inicio()).grid(row=2, column=0, padx=0  , pady=10)


    tk.Button(
    self,
    text=("Voltar a Tela Anterior"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.voltar_anterior()).grid(row=2, column=1, padx=0  , pady=10)


    
    self.focus_force()
    self.grab_set()
    


  def voltar_inicio(self):
    self.destroy()
    from agendamento.agenda import Agendamento
    Agendamento(self.master)


  def voltar_anterior(self):
    self.destroy()
    from agendamento.agenda import Editar_Agendamento
    Editar_Agendamento(self.master)


  


  def update_agendamento(self):
    # Validar se self.items[0] está presente
    if not self.items or not self.items[0]:
        showwarning("Entrada Inválida", "Item de agendamento não encontrado.", parent=self)
        return

    # Validar hora e minuto
    hour = self.hour_var.get()
    minute = self.minute_var.get()
    if hour == '--' or minute == '--':
        showwarning("Entrada Inválida", "Por favor, selecione uma hora válida.", parent=self)
        return

    selected_time = f"{hour}:{minute}"

    # Validar cliente
    cliente_nome = self.cliente_entry.get()
    if not cliente_nome or cliente_nome not in self.cliente_map:
        showwarning("Entrada Inválida", "Por favor, selecione um cliente válido.", parent=self)
        return

    # Validar serviço
    servico_nome = self.service_entry.get()
    if not servico_nome or servico_nome not in self.service_map:
      showwarning("Entrada Inválida", "Por favor, selecione um serviço válido.", parent=self)
      return

    # Validar funcionário
    func_nome = self.person_entry.get()
    if not func_nome or func_nome not in self.person_map:
        showwarning("Entrada Inválida", "Por favor, selecione um funcionário válido.", parent=self)
        return

    # Obter os IDs selecionados
    selected_id_cliente = self.cliente_map[cliente_nome]
    selected_id_servico = self.service_map[servico_nome]
    selected_id_func = self.person_map[func_nome]

    # Atualizar agendamento no banco de dados
   # Perguntar ao usuário se deseja confirmar a atualização
    if askyesno("Confirmação", "Tem certeza de que deseja atualizar este agendamento?", parent=self):
        try:
            dados.db_editar_agendamento(self.items[0], self.date_entry.get(), selected_time, selected_id_cliente, selected_id_servico, selected_id_func)
            showinfo("Sucesso", "Agendamento atualizado com sucesso!", parent=self)
            self.destroy()
            from agendamento.agenda import Agendamento
            Agendamento(self.master)
        except Exception as e:
            showwarning("Erro", f"Erro ao atualizar agendamento: {e}", parent=self)
 
    
  def _on_keyrelease(self, event):
    # Obtém o texto digitado pelo usuário
    value = event.widget.get().strip().lower()
    if value == '':
        data = self.cliente_names
    else:
        data = [item for item in self.cliente_names if value in item.lower()]

    # Atualiza os valores no combobox
    event.widget['values'] = data
    if data:
        event.widget.event_generate('<Down>')   
    