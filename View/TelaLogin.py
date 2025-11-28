from tkinter import *
from tkinter import ttk

class TelaLogin:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Login Hospitalar")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        
        ttk.Label(self.frm, text="Selecione seu perfil:").grid(column=0, row=0, columnspan=2, pady=5)
        
        #DEFAULT
        self.tipo = StringVar(value="PACIENTE") 

        #JOptionPane
        r1 = ttk.Radiobutton(self.frm, text="Sou Paciente", variable=self.tipo, value="PACIENTE")
        r2 = ttk.Radiobutton(self.frm, text="Sou Prof. Saúde", variable=self.tipo, value="PROFISSIONAL")
        r3 = ttk.Radiobutton(self.frm, text="Sou Funcionário", variable=self.tipo, value="FUNCIONARIO")
        
        r1.grid(column=0, row=1, columnspan=2, sticky=W)
        r2.grid(column=0, row=2, columnspan=2, sticky=W)
        r3.grid(column=0, row=3, columnspan=2, sticky=W)

        
        ttk.Label(self.frm, text="Login:").grid(column=0, row=4, pady=10)
        self.campo_login = ttk.Entry(self.frm)
        self.campo_login.grid(column=1, row=4)

        ttk.Label(self.frm, text="Senha:").grid(column=0, row=5)
        self.campo_senha = ttk.Entry(self.frm, show="*")
        self.campo_senha.grid(column=1, row=5)

     
        self.btn_entrar = ttk.Button(self.frm, text="Entrar")
        self.btn_entrar.grid(column=0, row=6, columnspan=2, pady=20)


    def set_action_botao(self, funcao_externa):
        self.btn_entrar.config(command=funcao_externa)

    def get_login(self):
        return self.campo_login.get()

    def get_senha(self):
        return self.campo_senha.get()

   
    def get_tipo_usuario(self):
        return self.tipo.get()