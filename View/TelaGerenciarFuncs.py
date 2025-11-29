from tkinter import *
from tkinter import ttk
from tkinter.ttk import Button, Entry

class TelaGerenciarFuncs:
    def __init__(self, root: Tk):
        self.janela = root

        self.janela.title("Gerenciamento de Funcionários")


        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()
        self.add_func_button: Button = ttk.Button(self.frm, text="Adicionar funcionário")
        self.remove_func_button: Button = ttk.Button(self.frm, text="Remover")
        self.search_func_button: Button = ttk.Button(self.frm, text="Consultar Informações de Funcionário")
        self.return_button: Button = ttk.Button(self.frm, text="Voltar")

        self.add_func_button.grid(column=0, row=0)
        self.remove_func_button.grid(column=0, row=1)
        self.search_func_button.grid(column=0, row=2)
        self.return_button.grid(column=0, row=3)

    def set_action_voltar(self, callback):
        self.return_button.config(command=callback)

    def set_action_adicionar_func(self, callback):
        self.add_func_button.config(command=callback)

    def set_action_remover_func(self, callback):
        self.remove_func_button.config(command=callback)

    def set_action_consultar_func(self, callback):
        self.search_func_button.config(command=callback)        
