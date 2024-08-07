import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk, simpledialog
from tkinter.messagebox import showinfo, showerror, askyesno, showwarning
from datetime import datetime, date
from time import strftime
from tkcalendar import DateEntry

class Editar_Agendamento(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)
  
    self.title("Editar Agendamento")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 8
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('1100x600+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")




    

    agenda_frame = tk.LabelFrame(self, text="Remarcar", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
    agenda_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew',columnspan=2)

    self.tv2 = ttk.Treeview(agenda_frame, columns=('ID', 'Nome Cliente', 'Data', 'Hora', 'Serviço', 'Funcionário'), show='headings')
    self.tv2.column("ID",minwidth=0,width=20, anchor=tk.CENTER)
    self.tv2.column("Nome Cliente",minwidth=0,width=100, anchor='w')
    self.tv2.column("Data",minwidth=0,width=60, anchor='w')
    self.tv2.column("Hora",minwidth=0,width=60, anchor='w')
    self.tv2.column("Serviço",minwidth=0,width=100, anchor='w')
    self.tv2.column("Funcionário",minwidth=0,width=100, anchor='w')

    self.tv2.heading('ID', text='ID')
    self.tv2.heading('Nome Cliente', text='Nome Cliente')
    self.tv2.heading('Data', text='Data')
    self.tv2.heading('Hora', text='Hora')
    self.tv2.heading('Serviço', text='Serviço')
    self.tv2.heading('Funcionário', text='Funcionário')
    self.tv2.pack(fill=tk.BOTH, expand=True)

    

    


    quandro2 = tk.LabelFrame(self, text = "Pesquisar Clientes",  background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
    quandro2.configure(height=1)
    quandro2.grid(row=0, column=0, padx=5, pady=10)

     # Date picker
    self.date_label = tk.Label(quandro2, text="Data", bg='#b4918f')
    self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    self.date_entry = DateEntry(quandro2, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
    self.date_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

    self.popular()

    self.pNome =tk.Entry(quandro2)
    self.pNome.bind('<Return>',(lambda event: self.pesquisaCliente()))
    self.pNome.grid(row=6, column=0, padx=5, pady=10)
    
    tk.Button(
    quandro2,
    text=("Buscar por cliente"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.pesquisaCliente()).grid(row=7, column=0, padx=5, pady=10)


    tk.Button(
    quandro2,
    text=("Buscar Por Data"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.popular_agendamento()).grid(row=7, column=1, padx=5, pady=10)



    tk.Button(
    self,
    text=("Voltar"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.voltar()).grid(row=2, column=0, padx=0  , pady=10)


    tk.Button(
    self,
    text=("Editar"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.update_agendamento()).grid(row=2, column=1, padx=0  , pady=10)


    tk.Button(
    self,
    text=("Deletar"),
    font=('TkMenuFont', 10),
    bg="#28393a",
    fg="white",
    cursor="hand2",
    activebackground="#badee2",
    activeforeground="black",
    bd = 5,
    
    command=lambda: self.deletar()).grid(row=2, column=2, padx=0  , pady=10)

    
    
    self.focus_force()
    self.grab_set()
    


  def pesquisaCliente(self):
    self.tv2.delete(*self.tv2.get_children())
    historico = dados.db_agenda_cliente(self.pNome.get())
    self.pNome.delete(0,tk.END)
    for a in historico:
      self.tv2.insert("","end", values=(a["id_agendamento"],a['nome_cliente'],a['data1'], a['hora'], a['nome_servico'], a['nome_funcionario']))


  def popular_agendamento(self):
    self.tv2.delete(*self.tv2.get_children())
    agendamento = dados.db_agenda(self.date_entry.get())

    for a in agendamento:
        self.tv2.insert("","end", values=(a["id_agendamento"],a['nome_cliente'],a['data1'], a['hora'], a['nome_servico'], a['nome_funcionario']))


  def popular(self):
    self.tv2.delete(*self.tv2.get_children())
    agendamento = dados.db_agenda(self.date_entry.get())

    for a in agendamento:
      self.tv2.insert("","end", values=(a["id_agendamento"],a['nome_cliente'],a['data1'], a['hora'], a['nome_servico'], a['nome_funcionario']))


  def voltar(self):
    self.destroy()
    from agendamento.agenda import Agendamento
    Agendamento(self.master)


  def select_time(self):
    try:
      # Verifica se um cliente foi selecionado
      if not self.tv.selection():
          showwarning("Entrada Inválida", "Por favor, selecione um cliente.", parent=self)
          return

      itemSelecionado = self.tv.selection()[0]
      items = self.tv.item(itemSelecionado, "value")

      # Verifica se uma hora foi selecionada
      hour = self.hour_var.get()
      minute = self.minute_var.get()
      if hour == '--' or minute == '--':
          showwarning("Entrada Inválida", "Por favor, selecione uma hora válida.", parent=self)
          return

      # Verifica se um nome de funcionário foi selecionado
      selected_name = self.person_entry.get()
      if selected_name not in self.person_map:
        showwarning("Entrada Inválida", "Por favor, selecione um funcionário válido.", parent=self)
        return
      
              # Verifica se um serviço foi selecionado
      selected_service = self.service_entry.get()
      if selected_service not in self.service_map:
        showwarning("Entrada Inválida", "Por favor, selecione um Serviço válido.", parent=self)
        return

      selected_id = self.person_map[selected_name]
      selected_id_service = self.service_map[selected_service]
      

      # Verifica se uma data foi selecionada
      if not self.date_entry.get():
          showwarning("Entrada Inválida", "Por favor, selecione uma data.", parent=self)
          return

      selected_time = f"{hour}:{minute}"
      date_str = self.date_entry.get()

      # Verifica se a data está no formato correto
      try:
          date_obj = datetime.strptime(date_str, "%d/%m/%Y")
      except ValueError:
          showwarning("Entrada Inválida", "Por favor, insira uma data válida no formato DD/MM/AAAA.", parent=self)
          return

      # Tenta criar o agendamento
      ja_existia, agendamento = dados.criar_agendamento(date_str, selected_time, items[0], selected_id_service, selected_id)

      mensagem = (f"O agendamento {date_obj.strftime('%d/%m/%Y')} {selected_time} já existia com o id {agendamento['id_agendamento']}."
                  if ja_existia else f"O Agendamento foi realizado para {date_obj.strftime('%d/%m/%Y')} {selected_time}.")
      showinfo("Informação", mensagem, parent=self)
      self.voltar()

    except Exception as e:

      showinfo("ERRO", f"Detalhes do erro: {e}", parent=self)

 
  def update_agendamento(self):
    try:
      if not self.tv2.selection():
        showwarning("Entrada Inválida", "Por favor, selecione um cliente.", parent=self)
        return

      
      
      itemSelecionado = self.tv2.selection()[0]
      items = self.tv2.item(itemSelecionado, "value")
      from agendamento.update_agendamento import Atualizar_Agendamento
      Atualizar_Agendamento(self.master,items )
      self.destroy()

    except Exception as e:
        showinfo("ERRO", f"Detalhes do erro: {e}", parent=self)

       
  def deletar(self):
    try:
      if not self.tv2.selection():
        showwarning("Entrada Inválida", "Por favor, selecione um cliente.", parent=self)
        return

      itemSelecionado = self.tv2.selection()[0]
      items = self.tv2.item(itemSelecionado, "value")
      
      if askyesno("Confirmação", "Tem certeza de que deseja excluir este agendamento?", parent=self):
        try:
            dados.apagar_agendamento(items[0], items[2])            
            showinfo("Sucesso", "Agendamento excluido com sucesso!", parent=self)
            self.destroy()
            from agendamento.agenda import Agendamento
            Agendamento(self.master)
        except Exception as e:
            showwarning("Erro", f"Erro ao atualizar agendamento: {e}", parent=self)
      

      from agendamento.agenda import Agendamento
      Agendamento(self.master)
      self.destroy()

    except Exception as e:
        showinfo("ERRO", f"Detalhes do erro: {e}", parent=self)
     

    
          
    