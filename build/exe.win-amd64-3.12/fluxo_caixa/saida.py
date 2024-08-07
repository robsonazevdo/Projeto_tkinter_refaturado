import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion
from tkcalendar import DateEntry
from operator import neg
from datetime import datetime, date

class Saida(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Fluxo de Caixa")
        self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = self.winfo_screenwidth() // 10
        y = int(self.winfo_screenheight() * 0.03)
        self.geometry('1000x690+' + str(x) + '+' + str(y))
        self.configure(background="#b4918f")

        quandro3 = tk.LabelFrame(self, text="Registrar Saída", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12, 'bold'))
        quandro3.grid(row=0, column=0, rowspan=2, sticky='nswe', padx=25, pady=25)
        quandro3.grid_columnconfigure(1, weight=1)
        quandro3.grid_rowconfigure(4, weight=1)

        dataLabel = tk.Label(quandro3, text="Data", bg="#b4918f", fg="white", font=('TkMenuFont', 10, 'bold'))
        dataLabel.grid(row=0, column=0, sticky='w', padx=5, pady=(5))

        self.pNome = DateEntry(quandro3, selectmode='day', locale='pt_br', date_pattern='dd/MM/yyyy')
        self.pNome.grid(row=0, column=1, sticky='ew', padx=5, pady=(5))

        descricaoLabel = tk.Label(quandro3, text="Descrição", bg="#b4918f", fg="white", font=('TkMenuFont', 10, 'bold'))
        descricaoLabel.grid(row=1, column=0, sticky='w', padx=5, pady=(5))

        self.descricao = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
        self.descricao.grid(row=1, column=1, sticky='ew', padx=5, pady=(5), columnspan=2)

        tk.Label(quandro3, text="Valor", bg="#b4918f", fg="white", font=('TkMenuFont', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=(5))

        vn = quandro3.register(self.validate_entry)
        self.valor = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10), validate="key", validatecommand=(vn, "%S", "%P"))
        self.valor.grid(row=2, column=1, sticky='ew', padx=5, pady=(5))

        tk.Label(quandro3, text="Observação", bg="#b4918f", fg="white", font=('TkMenuFont', 10)).grid(row=3, column=0, sticky='w', padx=5, pady=(5))

        self.obs = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
        self.obs.grid(row=3, column=1, sticky='ew', padx=5, pady=(5), columnspan=2)

        tk.Button(quandro3, text="Registrar Saída", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", bd=5, command=lambda: self.criar_saida()).grid(row=4, column=1, sticky='w', padx=5, pady=(5))

        quadroGridSaida = tk.LabelFrame(self, text="Saídas", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 14))
        quadroGridSaida.grid(row=0, column=1, sticky='nswe', padx=25, pady=25)
        quadroGridSaida.grid_columnconfigure(0, weight=1)
        quadroGridSaida.grid_rowconfigure(0, weight=1)

        self.tvs = ttk.Treeview(quadroGridSaida, columns=("id", "Data", "Nome", "Valor_Pago", "forma"), show="headings")
        self.tvs.column("id", minwidth=0, width=30, anchor=tk.W)
        self.tvs.column("Data", minwidth=15, width=70, anchor=tk.W)
        self.tvs.column("Nome", minwidth=15, width=150, anchor=tk.W)
        self.tvs.column("Valor_Pago", minwidth=0, width=100, anchor=tk.W)
        self.tvs.column("forma", minwidth=0, width=100, anchor=tk.W)
        self.tvs.heading("id", text="ID", anchor=tk.W)
        self.tvs.heading("Data", text="DATA", anchor=tk.W)
        self.tvs.heading("Nome", text="DESCRIÇÃO", anchor=tk.W)
        self.tvs.heading("Valor_Pago", text="VALOR PAGO", anchor=tk.W)
        self.tvs.heading("forma", text="OBSERVAÇÃO.", anchor=tk.W)
        self.tvs.pack(fill=tk.BOTH, expand=True)
        self.popular()

        quandro2 = tk.LabelFrame(self, text="Buscar Saída", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quandro2.grid(row=1, column=1, sticky='ew', padx=25, pady=25)
        quandro2.grid_columnconfigure(1, weight=1)

        self.date_out = DateEntry(quandro2, selectmode='day', locale='pt_br', date_pattern='dd/MM/yyyy')
        self.date_out.bind('<Return>', (lambda event: self.pesquisa_saida()))
        self.date_out.pack(side="left", padx=10)

        tk.Button(quandro2, text="Buscar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", bd=5, command=lambda: self.pesquisa_saida()).pack(side="left", padx=10)

        tk.Button(quandro2, text="  ar Todos", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", bd=5, command=lambda: self.popular()).pack(side="left", padx=10)

        tk.Button(quandro2, text="Editar", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", bd=5, command=lambda: self.editar_salvar()).pack(side="left", padx=10)

        self.focus_force()
        self.grab_set()

    def popular(self):
        self.tvs.delete(*self.tvs.get_children())
        saida = dados.db_listar_saida(datetime.strptime(self.pNome.get(), "%d/%m/%Y"))

        for s in saida:
            self.tvs.insert("", "end", values=(s['id_saida'], s["data"], s['descricao'], "%.2f" % s['valor_total'], s['observacao']))

    def pesquisa_saida(self):
        self.tvs.delete(*self.tvs.get_children())
        saida = dados.db_listar_saida(datetime.strptime(self.date_out.get(), "%d/%m/%Y"))

        for s in saida:
            self.tvs.insert("", "end", values=(s['id_saida'], s["data"], s['descricao'], "%.2f" % s['valor_total'], s['observacao']))

    def validate_entry(self, text, P):
        if len(P) > 10:
            return False

        if (
            all(char in "0123456789." for char in text) and  # all characters are valid
            "-" not in text[1:] and  # "-" is the first character or not present
            text.count(".") <= 1  # only 0 or 1 periods
        ):
            return True
        else:
            return False

    def criar_saida(self):
        d = self.pNome.get()
        if d == "" or self.descricao.get() == "" or self.valor.get() == "" or self.obs.get() == "":
            return showinfo(title=False, message="Preencha todos os campos", parent=self)

        else:
            dados.db_criar_saida(datetime.strptime(d, "%d/%m/%Y"), self.descricao.get().strip(" "), self.valor.get().strip(" "), self.obs.get().strip(" "))
            showinfo(title=False, message="Cadastro feito com sucesso", parent=self)
            self.descricao.delete(0, tk.END)
            self.valor.delete(0, tk.END)
            self.obs.delete(0, tk.END)

    def editar_salvar(self):
        try:
            itemS = self.tvs.selection()[0]
            valores = self.tvs.item(itemS, "value")
            _data = "{}/{}/{}".format(valores[1][8:10], valores[1][5:7], valores[1][:4])

            app = tk.Toplevel()
            app.title("Editar Saída")
            x = app.winfo_screenwidth() // 10
            y = int(app.winfo_screenheight() * 0.03)
            app.geometry('800x400+' + str(x) + '+' + str(y))
            app.configure(background="#b4918f")
            self.destroy()

            quandro3 = tk.LabelFrame(app, text="Registrar Saída", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12, 'bold'))
            quandro3.pack(fill=tk.BOTH, expand=True)

            def validate_entry(text, P):
                if len(P) > 10:
                    return False

                if (
                    all(char in "0123456789." for char in text) and  # all characters are valid
                    "-" not in text[1:] and  # "-" is the first character or not present
                    text.count(".") <= 1  # only 0 or 1 periods
                ):
                    return True
                else:
                    return False

            def alterar_saida():
                msg = askquestion("?", "Deseja Excluir o Atendimento do Cliente {0} do dia {1}".format(valores[2], valores[1]), parent=self)
                if msg == "yes":
                    d = pNome.get()
                    if d == "" or descricao.get() == "" or valor.get() == "" or obs.get() == "":
                        return showinfo(title=False, message="Preencha todos os campos", parent=self)

                    else:
                        dados.db_atualizar_saida(valores[0], datetime.strptime(d, "%d/%m/%Y"), descricao.get(), valor.get(), obs.get())
                        showinfo(title=False, message="Cadastro feito com sucesso", parent=self)
                        app.destroy()

            dataLabel = tk.Label(quandro3, text="Data", bg="#b4918f", fg="white", font=('TkMenuFont', 10, 'bold'))
            dataLabel.grid(row=0, column=0, sticky='w', padx=5, pady=(5))

            pNome = DateEntry(quandro3, selectmode='day', locale='pt_br', date_pattern='dd/MM/yyyy')
            pNome.grid(row=0, column=1, sticky='ew', padx=5, pady=(5))

            descricaoLabel = tk.Label(quandro3, text="Descrição", bg="#b4918f", fg="white", font=('TkMenuFont', 10, 'bold'))
            descricaoLabel.grid(row=1, column=0, sticky='w', padx=5, pady=(5))

            descricao = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
            descricao.grid(row=1, column=1, sticky='ew', padx=5, pady=(5), columnspan=2)

            tk.Label(quandro3, text="Valor", bg="#b4918f", fg="white", font=('TkMenuFont', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=(5))

            vn = quandro3.register(validate_entry)
            valor = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10), validate="key", validatecommand=(vn, "%S", "%P"))
            valor.grid(row=2, column=1, sticky='ew', padx=5, pady=(5))

            tk.Label(quandro3, text="Observação", bg="#b4918f", fg="white", font=('TkMenuFont', 10)).grid(row=3, column=0, sticky='w', padx=5, pady=(5))

            obs = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
            obs.grid(row=3, column=1, sticky='ew', padx=5, pady=(5), columnspan=2)

            tk.Button(quandro3, text="Registrar Saída", font=('TkMenuFont', 10), bg="#28393a", fg="white", cursor="hand2", activebackground="#badee2", activeforeground="black", bd=5, command=lambda: alterar_saida()).grid(row=4, column=1, sticky='w', padx=5, pady=(5))

            pNome.set_date(_data)
            descricao.insert(0, valores[2])
            valor.insert(0, valores[3])
            obs.insert(0, valores[4])

            app.focus_force()
            app.grab_set()

        except:
            showerror("ERRO!", "Precisa Selecionar um item", parent=self)
