from tkinter import *
from tkinter import ttk

class TelaAdicionarFunc:
    def __init__(self, root: Tk, funcoes: tuple):
        self.janela = root
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        self.janela.title("Adicionar func.")

        ttk.Label(self.frm, text="CPF funcionário", width=30).grid(column=0, row=0)
        self.cpf_field: ttk.Entry = ttk.Entry(self.frm, width=30)
        self.cpf_field.grid(column=1, row=0)

        ttk.Label(self.frm, text="Nome funcionário:", width=30).grid(column=0, row=1) 
        self.func_name_field: ttk.Entry = ttk.Entry(self.frm, width=30)
        self.func_name_field.grid(column=1, row=1)

        ttk.Label(self.frm, text="Func:", width=30).grid(column=0, row=3)
        self.func_selection: ttk.Combobox = ttk.Combobox(self.frm, width=28, state='readonly')
        self.func_selection['values'] = funcoes
        self.func_selection.grid(column=1, row=3)

        self.return_button: ttk.Button = ttk.Button(self.frm, text="voltar")
        self.return_button.grid(column=0, row=4, columnspan=2)

    def set_return_action(self, callback):
        self.return_button.config(command=callback)

    def get_cpf_field(self):
        self.cpf_field.get()

    def get_name_field(self):
        self.func_name_field.get()

    def get_func_field(self):
        self.func_selection.get()
