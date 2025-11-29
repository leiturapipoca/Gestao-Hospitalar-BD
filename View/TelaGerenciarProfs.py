from tkinter import *
from tkinter import ttk
from tkinter.ttk import Button, Entry

class TelaGerenciarProfs:
    def __init__(self, root: Tk):
        self.janela = root

        self.janela.title("Gerenciamento de Profissionais de Saúde")

        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()
        self.add_prof_button: Button = ttk.Button(self.frm, text="Adicionar profissional de saúde")
        self.remove_prof_button: Button = ttk.Button(self.frm, text="Remover profissional de saúde")
        self.search_prof_button: Button = ttk.Button(self.frm, text="Consultar informações de profissional")
        self.return_button: Button = ttk.Button(self.frm, text="Voltar")

        self.add_prof_button.grid(column=0, row=0)
        self.remove_prof_button.grid(column=0, row=1)
        self.search_prof_button.grid(column=0, row=2)
        self.return_button.grid(column=0, row=3)

    def set_action_voltar(self, callback):
        self.return_button.config(command=callback)

    def set_action_adicionar_prof(self, callback):
        self.add_prof_button.config(command=callback)

    def set_action_remover_prof(self, callback):
        self.remove_prof_button.config(command=callback)

    def set_action_consultar_prof(self, callback):
        self.search_prof_button.config(command=callback)
