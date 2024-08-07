import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askquestion
from tkcalendar import DateEntry
from operator import neg
from datetime import datetime, date
import calendario



class Contas_a_Pagar(tk.Toplevel):
  def __init__(self, parent):
    super().__init__(parent)

    
    self.title("Contas a pagar")
    self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
    x = self.winfo_screenwidth() // 8
    y = int(self.winfo_screenheight() * 0.1)
    self.geometry('900x600+' + str(x) + '+' + str(y) )
    self.configure(background="#b4918f")
    
    s = dados.db_listar_saida2()
    events = {}
    for x in s:
        events.setdefault(x['data'][:10], []).append(( x['descricao'] + ' ' + str(f"{x['valor_total']:.2f}"),'reminder'))
    

    agenda = calendario.Agenda(self, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy',firstweekday="sunday")
    
    for k in events.keys():
        date=datetime.strptime(k,"%Y-%m-%d").date()
        for v in range(len(events[k])):
            agenda.calevent_create(date, events[k][v][0], events[k][v][1])


    

    agenda.tag_config('reminder', background="#8B0000", foreground='white')
    agenda.pack(fill="both", expand=True)

    
            