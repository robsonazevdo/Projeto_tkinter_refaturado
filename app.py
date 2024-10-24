import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import Banco as dados
from PIL import ImageTk, Image
from cliente.pequisar_cliente import Pesquisar_Cliente
from atendimento.novo_atendimento import Novo_Atendimento
from atendimento.pesquisar_atendimento import Pesquisar_Atendimento
from atendimento.deletar_atendimento import Deletar_Atendimento 
from fluxo_caixa.entradaxsaida import Entrada_Saida
from fluxo_caixa.saida import Saida
from fluxo_caixa.contas_a_pagar import Contas_a_Pagar      
from agendamento.agenda import Agendamento
from backup.backup import Backup
from servico.servico import Servico
from funcionario.funcionario import Funcionario
from comanda.comanda import BeautySalon
from historico.historico import Historico_Atendimento


import os
import sys




class App(tk.Tk):
  def __init__(self):
    super().__init__()


  

    # configure the root window
    self.title('Fluxo Mensal')

    x = self.winfo_screenwidth() // 240

    y = int(self.winfo_screenheight() * 0.0)
    self.attributes('-fullscreen',True)
    self.geometry('1360x728+' + str(x) + '+' + str(y))


    self.frame1 = Frame1(self)
    self.frame2 = Frame2(self)
    self.show_frame(self.frame1)

  def show_frame(self, frame):
    try:
        frame.tkraise()
    except tk.TclError as e:
           ("Erro ao tentar mostrar o frame:", e)


class Frame1(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)



        self.parent = parent

        #root.eval("tk::PlaceWindow . center")
        x = self.winfo_screenwidth() // 240

        y = int(self.winfo_screenheight() * 0.0)
        # self.attributes('-fullscreen',True)
        self.config(width=800, height=600)
        self.place(x=0, y=0)

        
        frame1 = tk.Frame(self, width=1360, height=728, bg="#b4918f")
        
        frame1.grid(row=0, column=0)
    



        frame1.pack_propagate(False)
        logo_path = self.resource_path('assets/Logo-colorido.png')
        image = Image.open('assets/Logo-colorido.png')
        resize_image = image.resize((200, 200))
        logo_img = ImageTk.PhotoImage(resize_image)

        logo_widget = tk.Label(frame1, image=logo_img, bg="#b4918f")
        logo_widget.image = logo_img
        logo_widget.pack()


        l1 = tk.Label(
        frame1,
        text="Logar no Sistema",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 14)
        ).pack()


        tk.Label(
            frame1,
            text="Usuário",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 14),
            padx=15,
            pady=15 
            ).pack()
        email = tk.Entry(frame1,width=65, font=('TkMenuFont', 10))
        email.place(x=60, y=60)
        email.focus()
        email.bind('<Return>',(lambda event: self.load_frame2(email.get(),password.get())))
        email.pack()


        tk.Label(
            frame1,
            text="Senha",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 14),
            padx=15,
            pady=15 
            ).pack()
        password = tk.Entry(frame1,show="*", width=65, font=('TkMenuFont', 10))
        password.bind('<Return>',(lambda event: self.load_frame2(email.get(),password.get().strip(" "))))
        password.place(x=60, y=60)
        password.pack()


        button = tk.Button(
        frame1,
        text=("LOGIN"),
        font=('TkMenuFont', 15),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
            bd = 5,
        command=lambda: self.load_frame2(email.get(),password.get())
        )

        button.pack(pady=(80, 0))

        button_close = tk.Button(frame1, text="SAIR", font=('TkMenuFont', 15),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,command=self.parent.destroy)

        button_close.pack(pady=(60, 0), padx=(0, 0))
        

    def load_frame2(self, email, password):
        g = dados.db_fazer_login_admin(email, password)
        
        if g is None:
            showerror(title=False, message="Email ou Senha Inválido")
        elif g['email'] == email and g['senha'] == password:
            self.parent.frame2 = Frame2(self.parent)  # Recriar Frame2 ao logar
            self.parent.frame2.grid(row=0, column=0, sticky='nsew')
            self.parent.show_frame(self.parent.frame2)
            self.parent.frame2.create_menu()
        else:
            showerror(title=False, message="Email ou Senha Inválido")

    def resource_path(self,relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
        


class Frame2(tk.Frame):
    
    def __init__(self,parent):
        super().__init__(parent)


    
        self.config(width=800, height=600)
        self.place(x=0, y=0)    
            
  
     
        frame2 = tk.Frame(self, width=1360, height=728, bg="#b4918f")
        frame2.grid(row=0, column=1)
        # self.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        logo_path = self.resource_path("assets/salao-de-beleza.jpeg")
        image2 = Image.open("assets/salao-de-beleza.jpeg")
        resize_image2 = image2.resize((1360, 728))
        logo_img2 = ImageTk.PhotoImage(resize_image2)
        
        logo_widget2 = tk.Label(frame2, image=logo_img2)
        logo_widget2.image = logo_img2
        logo_widget2.place(x=0, y=0)

        

        
    def create_menu(self):
    
        barraMenu = tk.Menu(self.master)
        menuContatos = tk.Menu(barraMenu, tearoff=0)
        menuContatos.add_command(label="Cliente",command=self.pesquisar_cliente)
        menuContatos.add_command(label="Serviço",command=self.novo_servico)
        menuContatos.add_command(label="Funcionário",command=self.novo_funcionario)
        menuContatos.add_separator()
        menuContatos.add_command(label="Logout",command=self.logout)
        menuContatos.add_command(label="Fechar",command=self.master.destroy)
        barraMenu.add_cascade(label="Cadastro",menu=menuContatos)
        

        # menuAtendimento = tk.Menu(barraMenu, tearoff=0)
        # menuAtendimento.add_command(label="Novo",command=self.novo_atendimento)
        # menuAtendimento.add_command(label="Pesquisar",command=self.pesquisar_atendimento)
        # menuAtendimento.add_command(label="Deletar",command=self.deletar_atendimento)
    
        # barraMenu.add_cascade(label="Atendimento ",menu=menuAtendimento)
        
        
        relatorioMenu = tk.Menu(barraMenu, tearoff=0)
        relatorioMenu.add_command(label="Entrada x Saída", command=self.entradaxsaida)
        relatorioMenu.add_command(label="Saída", command=self.saida)
        relatorioMenu.add_command(label="Contas a Pagar", command=self.contas_a_pagar)
        barraMenu.add_cascade(label="Fluxo de caixa", menu=relatorioMenu)


        comanda_Menu = tk.Menu(barraMenu, tearoff=0)
        comanda_Menu.add_command(label="Comanda", command=self.comanda)
        barraMenu.add_cascade(label="Comanda", menu=comanda_Menu)
        
        
        AgendaMenu = tk.Menu(barraMenu, tearoff=0)
        AgendaMenu.add_command(label="Agendamento", command=self.agendamento)
        barraMenu.add_cascade(label="Agenda", menu=AgendaMenu)


        historico_Menu = tk.Menu(barraMenu, tearoff=0)
        historico_Menu.add_command(label="Histórico", command=self.historico)
        barraMenu.add_cascade(label="Histórico Atendimento", menu=historico_Menu)


        backup_Menu = tk.Menu(barraMenu, tearoff=0)
        backup_Menu.add_command(label="Backup", command=self.fazer_backup)
        barraMenu.add_cascade(label="Backup", menu=backup_Menu)


        self.master.config(menu=barraMenu)

        
       
    
    def logout(self):
        self.master.config(menu="")  # Remover o menu
        self.destroy()
        app.frame1 = Frame1(self.master)
        app.show_frame(app.frame1)

    def novo_servico(self):
       Servico(self.master)

    def novo_funcionario(self):
       Funcionario(self.master)

    def pesquisar_cliente(self):
        Pesquisar_Cliente(self.master)
              
    def novo_atendimento(self):
        Novo_Atendimento(self, self.on_toplevel1_close)
 
    def pesquisar_atendimento(self):
        Pesquisar_Atendimento(self.master)

    def deletar_atendimento(self):
        Deletar_Atendimento(self.master)

    def entradaxsaida(self):
        Entrada_Saida(self.master)

    def saida(self):
        Saida(self.master)

    def contas_a_pagar(self):
        Contas_a_Pagar(self.master)

    def agendamento(self):
        Agendamento(self.master)
 
    def on_toplevel1_close(self, data):
        return data

    def resource_path(self,relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def fazer_backup(self):
        Backup(self.master)

    def comanda(self):
        BeautySalon(self.master)

    def historico(self):
        Historico_Atendimento(self.master)



        
  
       

if __name__ == "__main__":
  app = App()
  app.mainloop()
  dados.db_inicializar()
