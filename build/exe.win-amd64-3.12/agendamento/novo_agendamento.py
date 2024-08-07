import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion, showwarning
from datetime import datetime, date
from tkcalendar import DateEntry
import Banco as dados

class Novo_Agendamento(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Novo Agendamento")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = self.winfo_screenwidth() // 8
        y = int(self.winfo_screenheight() * 0.1)
        self.geometry('1100x600+' + str(x) + '+' + str(y))
        self.configure(background="#b4918f")

        right_frame = tk.LabelFrame(self, text="Clientes", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.tv = ttk.Treeview(right_frame, columns=('ID', 'Nome', 'Telefone'), show='headings')
        self.tv.heading('ID', text='ID')
        self.tv.heading('Nome', text='Nome')
        self.tv.heading('Telefone', text='Telefone')
        self.tv.pack(fill=tk.BOTH, expand=True)
        self.popular()

        left_frame = tk.LabelFrame(self, text="Agendar", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        self.date_label = tk.Label(left_frame, text="Data", bg='#b4918f', fg='white', font=("Helvetica", 12))
        self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.date_entry = DateEntry(left_frame, selectmode='day', locale='pt_br', date_pattern='dd/MM/yyyy')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Adicionando validação para a data
        self.date_entry.bind("<<DateEntrySelected>>", self.validate_date)

        service = dados.db_listar_servico()
        self.service_map = {serv['nome_servico']: serv['id_servico'] for serv in service}
        service_names = list(self.service_map.keys())

        self.service_label = tk.Label(left_frame, text="Escolha o serviço", bg='#b4918f', fg='white', font=("Helvetica", 12))
        self.service_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.service_entry = ttk.Combobox(left_frame, values=service_names)
        self.service_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        funcionario = dados.db_listar_funcionarios()
        self.person_label = tk.Label(left_frame, text="Quem irá Realizar?", bg='#b4918f', fg='white', font=("Helvetica", 12))
        self.person_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.person_map = {func['nome']: func['id_funcionario'] for func in funcionario}
        person_names = list(self.person_map.keys())

        self.person_entry = ttk.Combobox(left_frame, values=person_names)
        self.person_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.label = tk.Label(left_frame, text="Escolha a hora", bg='#b4918f', fg='white', font=("Helvetica", 12))
        self.label.grid(row=3, column=0, pady=5, sticky='w')
        self.hour_var = tk.StringVar()
        self.hour_combobox = ttk.Combobox(left_frame, textvariable=self.hour_var, values=[f'{i:02d}' for i in range(7, 21)], state="readonly", width=3)
        self.hour_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.hour_combobox.set('--')
        self.minute_var = tk.StringVar()
        self.minute_combobox = ttk.Combobox(left_frame, textvariable=self.minute_var, values=[f'{i:02d}' for i in range(0, 60, 15)], state="readonly", width=3)
        self.minute_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.minute_combobox.set('--')

        self.select_button = tk.Button(left_frame, text="Selecionar", font=('TkMenuFont', 10),
                                       bg="#28393a",
                                       fg="white",
                                       cursor="hand2",
                                       activebackground="#badee2",
                                       activeforeground="black",
                                       bd=5,
                                       command=self.criar_agendamento)
        self.select_button.grid(row=6, column=0, columnspan=2, pady=10)

        quandro2 = tk.LabelFrame(self, text="Pesquisar Clientes", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quandro2.configure(height=1)
        quandro2.grid(row=1, column=0, padx=5, pady=10)

        self.pNome = tk.Entry(quandro2)
        self.pNome.bind('<Return>', (lambda event: self.pesquisaCliente()))
        self.pNome.grid(row=0, column=0, padx=5, pady=10)

        tk.Button(quandro2,
                  text="Pesquisar",
                  font=('TkMenuFont', 10),
                  bg="#28393a",
                  fg="white",
                  cursor="hand2",
                  activebackground="#badee2",
                  activeforeground="black",
                  bd=5,
                  command=lambda: self.pesquisaCliente()).grid(row=7, column=0, padx=5, pady=10)

        tk.Button(quandro2,
                  text="Mostrar Todos",
                  font=('TkMenuFont', 10),
                  bg="#28393a",
                  fg="white",
                  cursor="hand2",
                  activebackground="#badee2",
                  activeforeground="black",
                  bd=5,
                  command=lambda: self.popular()).grid(row=7, column=1, padx=5, pady=10)

        tk.Button(self,
                  text="Voltar",
                  font=('TkMenuFont', 10),
                  bg="#28393a",
                  fg="white",
                  cursor="hand2",
                  activebackground="#badee2",
                  activeforeground="black",
                  bd=5,
                  command=lambda: self.voltar()).grid(row=2, column=0, padx=0, pady=10)

        self.focus_force()
        self.grab_set()

    def pesquisaCliente(self):
        self.tv.delete(*self.tv.get_children())
        historico = dados.db_historico_cliente(self.pNome.get())
        self.pNome.delete(0, tk.END)
        for c in historico:
            self.tv.insert("", "end", values=(c["id_cliente"], c['nome'], c['telefone']))

    def popular(self):
        self.tv.delete(*self.tv.get_children())
        cliente = dados.db_listar_cliente()
        for c in cliente:
            self.tv.insert("", "end", values=(c["id_cliente"], c['nome'], c['telefone']))

    def voltar(self):
        self.destroy()
        from agendamento.agenda import Agendamento
        Agendamento(self.master)

    def criar_agendamento(self):
        try:
            if not self.tv.selection():
                showwarning("Entrada Inválida", "Por favor, selecione um cliente.", parent=self)
                return

            itemSelecionado = self.tv.selection()[0]
            items = self.tv.item(itemSelecionado, "value")

            hour = self.hour_var.get()
            minute = self.minute_var.get()
            if hour == '--' or minute == '--':
                showwarning("Entrada Inválida", "Por favor, selecione uma hora válida.", parent=self)
                return

            selected_name = self.person_entry.get()
            if selected_name not in self.person_map:
                showwarning("Entrada Inválida", "Por favor, selecione um funcionário válido.", parent=self)
                return

            selected_service = self.service_entry.get()
            if selected_service not in self.service_map:
                showwarning("Entrada Inválida", "Por favor, selecione um Serviço válido.", parent=self)
                return

            selected_id = self.person_map[selected_name]
            selected_id_service = self.service_map[selected_service]

            if not self.date_entry.get():
                showwarning("Entrada Inválida", "Por favor, selecione uma data.", parent=self)
                return

            selected_time = f"{hour}:{minute}"
            date_str = self.date_entry.get()

            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                showwarning("Entrada Inválida", "Por favor, insira uma data válida no formato DD/MM/AAAA.", parent=self)
                return

            ja_existia, agendamento = dados.criar_agendamento(date_str, selected_time, items[0], selected_id_service, selected_id)

            mensagem = (f"O agendamento {date_obj.strftime('%d/%m/%Y')} {selected_time} já existia com o id {agendamento['id_agendamento']}."
                        if ja_existia else f"O Agendamento foi realizado para {date_obj.strftime('%d/%m/%Y')} {selected_time}.")
            showinfo("Informação", mensagem, parent=self)
            self.voltar()

        except Exception as e:
            showinfo("ERRO", f"Detalhes do erro: {e}", parent=self)

    def validate_date(self, event):
        selected_date = self.date_entry.get_date()
        today = date.today()
        if selected_date < today:
            showerror("Data Inválida", "A data selecionada não pode ser anterior ao dia de hoje.", parent=self)
            self.date_entry.set_date(today)

