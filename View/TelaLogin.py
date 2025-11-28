from tkinter import *
from tkinter import ttk

class TelaLogin:
    
    def __init__(self, master):

        self.janela = master
        self.janela.title("Login do Sistema")
        
        #JPanel
        self.frm = ttk.Frame(self.janela, padding=10)
        self.frm.grid()

        
        ttk.Label(self.frm, text="Login:").grid(column=1, row=0)
        ttk.Label(self.frm, text="Nome: ").grid(column=0, row=1)
        ttk.Label(self.frm, text="Senha: ").grid(column=0, row=2)
     
        #JTextField
        self.campo_nome = ttk.Entry(self.frm)
        self.campo_nome.grid(column=1, row=1)
        self.campo_senha = ttk.Entry(self.frm, show="*")
        self.campo_senha.grid(column=1, row=2)


        #JButton
        self.btn_login = ttk.Button(self.frm, text="Login")
        self.btn_login.grid(column=0, row=4)
        
        ttk.Button(self.frm, text="Quit", command=self.janela.destroy).grid(column=1, row=4)
        
    #Passa o controle pro controller
    def set_action_botao(self, funcao_externa):
        self.btn_login.config(command=funcao_externa)


    def get_login(self):
        return self.campo_nome.get()

    def get_senha(self):
        return self.campo_senha.get()
        