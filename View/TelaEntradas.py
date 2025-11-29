from tkinter import *
from tkinter import ttk

class TelaEntradas:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Registrar Nova Entrada")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="Nova Admissão Hospitalar", font=("Arial", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=15)

      
        ttk.Label(self.frm, text="CPF do Paciente:").grid(column=0, row=1, sticky=W, pady=5)
        self.campo_cpf = ttk.Entry(self.frm, width=30)
        self.campo_cpf.grid(column=1, row=1, sticky=EW)

       
        ttk.Label(self.frm, text="Hospital Vinculado:").grid(column=0, row=2, sticky=W, pady=5)
        self.campo_cnes = ttk.Entry(self.frm, width=30)
        self.campo_cnes.grid(column=1, row=2, sticky=EW)

        # --- Botões ---
        self.btn_salvar = ttk.Button(self.frm, text="CONFIRMAR ENTRADA")
        self.btn_salvar.grid(column=0, row=4, columnspan=2, pady=20, sticky=EW)
        
        self.btn_voltar = ttk.Button(self.frm, text="Cancelar / Voltar")
        self.btn_voltar.grid(column=0, row=5, columnspan=2, sticky=EW)

   

    def set_action_salvar(self, funcao):
        self.btn_salvar.config(command=funcao)

    def set_action_voltar(self, funcao):
        self.btn_voltar.config(command=funcao)

    def get_cpf(self):
        return self.campo_cpf.get()

    def get_cnes(self):
        return self.campo_cnes.get()
    
    #Pega cnes automatico
    def preencher_cnes(self, valor_cnes):
       
        self.campo_cnes.delete(0, END)  
        self.campo_cnes.insert(0, valor_cnes)#Preenche
        self.campo_cnes.config(state='readonly')#Trava 