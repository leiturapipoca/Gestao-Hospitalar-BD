from tkinter import *
from tkinter import ttk

class TelaProcedimentos:
    def __init__(self, master, procedures: tuple):
        self.janela = master
        self.janela.title("Registrar Procedimento")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="Novo Procedimento Médico", font=("Arial", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=15)

        # Campo: Nome da Doença
        ttk.Label(self.frm, text="Nome da Doença:").grid(column=0, row=1, sticky=W, pady=5)
        self.campo_doenca = ttk.Entry(self.frm, width=30)
        self.campo_doenca.grid(column=1, row=1, sticky=EW)

        # Campo: CPF do Médico
        ttk.Label(self.frm, text="CPF do Médico:").grid(column=0, row=2, sticky=W, pady=5)
        self.campo_cpf_medico = ttk.Entry(self.frm, width=30)
        self.campo_cpf_medico.grid(column=1, row=2, sticky=EW)

        # Campo: Tipo de Procedimento (Combobox)
        ttk.Label(self.frm, text="Tipo de Procedimento:").grid(column=0, row=3, sticky=W, pady=5)
        self.combo_procedimento = ttk.Combobox(self.frm, width=28, state='readonly')
        self.combo_procedimento['values'] = procedures
        self.combo_procedimento.grid(column=1, row=3, sticky=EW)

        ttk.Label(self.frm, text="Número da Sala:").grid(column=0, row=4, sticky=W, pady=5)
        self.campo_sala = ttk.Entry(self.frm, width=30)
        self.campo_sala.grid(column=1, row=4, sticky=EW)

        # Botões
        self.btn_salvar = ttk.Button(self.frm, text="CONFIRMAR PROCEDIMENTO")
        self.btn_salvar.grid(column=0, row=5, columnspan=2, pady=20, sticky=EW)
        
        self.btn_voltar = ttk.Button(self.frm, text="Voltar")
        self.btn_voltar.grid(column=0, row=6, columnspan=2, sticky=EW)

    def set_action_salvar(self, funcao):
        self.btn_salvar.config(command=funcao)

    def set_action_voltar(self, funcao):
        self.btn_voltar.config(command=funcao)

    def get_doenca(self):
        return self.campo_doenca.get()

    def get_cpf_medico(self):
        return self.campo_cpf_medico.get()

    def get_procedimento(self):
        return self.combo_procedimento.get()

    def get_sala(self):
        return self.campo_sala.get()

    def preencher_sala(self, valor):
        self.campo_sala.delete(0, END)
        self.campo_sala.insert(0, valor)
        self.campo_sala.config(state='readonly')

    def carregar_procedimentos(self, lista_procedimentos):
        """Atualiza a lista de procedimentos disponíveis no combobox"""
        self.combo_procedimento['values'] = lista_procedimentos
