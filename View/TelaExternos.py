from tkinter import *
from tkinter import ttk

class TelaExternos:
    def __init__(self, master, usuario):
        self.janela = master
        self.janela.title(f"Bem vindo, {usuario}")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

       
        ttk.Label(self.frm, text=f"Olá, {usuario}", font=("Arial", 14)).grid(column=0, row=0, pady=10)
        ttk.Label(self.frm, text="O que deseja fazer?").grid(column=0, row=1, pady=5)

       
        self.btn_dados = ttk.Button(self.frm, text="Consultar meus dados")
        self.btn_dados.grid(column=0, row=2, pady=10, sticky=EW)

       
        self.btn_pacientes = ttk.Button(self.frm, text="Acesssar meu histórico")
        self.btn_pacientes.grid(column=0, row=3, pady=10, sticky=EW)

       
        #self.btn_profissionais = ttk.Button(self.frm, text="Gerenciar Profissionais")
        #self.btn_profissionais.grid(column=0, row=4, pady=10, sticky=EW)

        #self.btn_entradas = ttk.Button(self.frm, text="Registrar Entradas")
        #self.btn_entradas.grid(column=0, row=5, pady=10, sticky=EW)

        #self.btn_hospitais = ttk.Button(self.frm, text="Gerenciar Hospitais")
        #self.btn_hospitais.grid(column=0, row=6, pady=10, sticky=EW)
        

      
        ttk.Button(self.frm, text="Sair", command=self.janela.destroy).grid(column=0, row=7, pady=20)

    
    def configurar_navegacao(self, comando_dados, comando_historico):
       
        self.btn_dados.config(command=comando_dados)
        self.btn_pacientes.config(command=comando_historico)
      