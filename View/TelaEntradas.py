from tkinter import *
from tkinter import ttk

class TelaEntradas:
    # sala e opcional
    def __init__(self, master, salas_livres=()):
        self.janela = master
        self.janela.title("Registrar Nova Entrada")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="Nova Admissão Hospitalar", font=("Arial", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=15)

        # cpf
        ttk.Label(self.frm, text="CPF do Paciente:").grid(column=0, row=1, sticky=W, pady=5)
        self.campo_cpf = ttk.Entry(self.frm, width=30)
        self.campo_cpf.grid(column=1, row=1, sticky=EW)

        # hospital 
        ttk.Label(self.frm, text="Hospital Vinculado:").grid(column=0, row=2, sticky=W, pady=5)
        self.campo_cnes = ttk.Entry(self.frm, width=30)
        self.campo_cnes.grid(column=1, row=2, sticky=EW)

        # descrição
        ttk.Label(self.frm, text="Descrição:").grid(column=0, row=3, sticky=W, pady=5)
        self.description = ttk.Entry(self.frm, width=30)
        self.description.grid(column=1, row=3, sticky=EW)

        # sala
        ttk.Label(self.frm, text="Alocar Sala:").grid(column=0, row=4, sticky=W, pady=5)
        self.combo_sala = ttk.Combobox(self.frm, width=28, state='readonly')
        
        # Preenche com o que veio do Controller 
        self.combo_sala['values'] = salas_livres 
        self.combo_sala.grid(column=1, row=4, sticky=EW)

        #Botões 
        self.btn_salvar = ttk.Button(self.frm, text="CONFIRMAR ENTRADA")
        self.btn_salvar.grid(column=0, row=5, columnspan=2, pady=20, sticky=EW)
        
        self.btn_voltar = ttk.Button(self.frm, text="Voltar")
        self.btn_voltar.grid(column=0, row=6, columnspan=2, sticky=EW)

    def set_action_salvar(self, funcao): self.btn_salvar.config(command=funcao)
    def set_action_voltar(self, funcao): self.btn_voltar.config(command=funcao)

    def get_cpf(self): return self.campo_cpf.get()
    def get_cnes(self): return self.campo_cnes.get()
    def get_description(self): return self.description.get()
    def get_sala(self): return self.combo_sala.get()
    
    def preencher_cnes(self, valor_cnes):
        self.campo_cnes.config(state='normal')
        self.campo_cnes.delete(0, END)  
        self.campo_cnes.insert(0, valor_cnes)
        self.campo_cnes.config(state='readonly')