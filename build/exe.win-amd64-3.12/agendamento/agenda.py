import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk, simpledialog
from tkinter.messagebox import showinfo, showerror, askquestion
from operator import neg
from datetime import datetime, date
from agendamento.novo_agendamento import Novo_Agendamento
from agendamento.editar_agendamento import Editar_Agendamento
from tkcalendar import DateEntry

class Agendamento(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
    
        self.title("Agendamento")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = self.winfo_screenwidth() // 8
        y = int(self.winfo_screenheight() * 0.1)
        self.geometry('1100x600+' + str(x) + '+' + str(y) )
        self.configure(bg="#b4918f")

        # Frame fixo para os controles
        self.fixed_frame = tk.Frame(self, bg="#b4918f")
        self.fixed_frame.pack(side=tk.TOP, fill=tk.X)

        # Canvas para a área rolável
        self.canvas = tk.Canvas(self, bg="#b4918f")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#b4918f")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<MouseWheel>", self._on_mouse_wheel)

        # Adicionar data e botões no frame fixo
        self.data = DateEntry(self.fixed_frame, selectmode='day', locale='pt_br', date_pattern='dd/MM/yyyy')
        self.data.grid(row=0, column=0, padx=10, pady=10)

        self.string_variable = tk.StringVar()
        self.dia_semana = tk.Label(self.fixed_frame, textvariable=self.string_variable, width=20, background='#28393a', foreground='white')
        self.dia_semana.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(
            self.fixed_frame,
            text="Buscar",
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5,
            command=lambda: self.buscar_agendamento()
        ).grid(row=0, column=1, padx=10, pady=10)

        tk.Button(
            self.fixed_frame,
            text="Inserir Novo",
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5,
            command=lambda: self.novo_agendamento()
        ).grid(row=0, column=2, padx=10, pady=10)

        tk.Button(
            self.fixed_frame,
            text="Remarcar",
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd=5,
            command=lambda: self.editar_agendamento()
        ).grid(row=0, column=3, padx=10, pady=10)

        self.agendamento = dados.db_agenda(self.data.get())

        horarios = self.generate_horarios()
       
        for i, horario in enumerate(horarios):
            label = tk.Label(self.scrollable_frame, text=horario, width=5, background='white')
            label.grid(row=i+1, column=0)

        funcionarios = dados.db_listar_funcionarios()
        for cont, func in enumerate(funcionarios, start=1):
            label = tk.Label(self.scrollable_frame, text=func['nome'], width=35, background='#b4918f')
            label.grid(row=0, column=cont)

        self.entries = {}
        for col, funcionario in enumerate(funcionarios):
            funcionario_label = tk.Label(self.scrollable_frame, text=funcionario['nome'], bg='#b4918f')
            funcionario_label.grid(row=0, column=col+1, padx=5, pady=5)
            for row, horario in enumerate(horarios):
                self.entry = tk.Entry(self.scrollable_frame)
                self.entry.grid(row=row+1, column=col+1, padx=5, pady=5)
                self.entries[(funcionario['nome'], horario)] = self.entry

        self.populate_agendamentos()
        self.mostrar_dia_semana()
        
        

        self.focus_force()
        self.grab_set()

    def novo_agendamento(self):
        Novo_Agendamento(self.master)
        self.destroy()

    def editar_agendamento(self):
        Editar_Agendamento(self.master)
        self.destroy()

    def generate_horarios(self):
        horarios = []
        for h in range(7, 21):
            horarios.append(f"{h:02d}:00")
            horarios.append(f"{h:02d}:30")
        return horarios

    def populate_agendamentos(self, selected_date=None):
        for (nome_funcionario, hora), self.entry in self.entries.items():
            self.entry.delete(0, tk.END)  # Limpa o campo de entrada
        for agenda in self.agendamento:
            if selected_date and agenda['data1'] != selected_date:
                continue
            key = (agenda['nome_funcionario'], agenda['hora'])
            if key in self.entries:
                self.entries[key].insert(0, agenda['nome_cliente'] + " - " + agenda['nome_servico'])

    def buscar_agendamento(self):
        self.agendamento = dados.db_agenda(self.data.get())
        self.populate_agendamentos()
        self.mostrar_dia_semana()

    def _on_mouse_wheel(self, event):
        try:
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")
        except Exception as e:
            print(f"Erro ao rolar: {e}")

    def mostrar_dia_semana(self):
        data_string = self.data.get()
        try:
            # Converta a string para um objeto datetime
            data = datetime.strptime(data_string, '%d/%m/%Y')
            # Obtenha o dia da semana em português
            dias_da_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
            dia_semana = dias_da_semana[data.weekday()]
            # Atualize o valor da StringVar para exibir no Label
            self.string_variable.set(dia_semana)
        except ValueError:
            self.string_variable.set("Por favor, selecione uma data válida.")
