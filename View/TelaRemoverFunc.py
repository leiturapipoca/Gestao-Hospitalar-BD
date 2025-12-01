from tkinter import *
from tkinter import ttk

class TelaRemoverFunc:
    def __init__(self, root):
        self.janela = root
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="CPF funcionário:").grid(column=0, row=0)
        self.cpf_field: ttk.Entry = ttk.Entry(self.frm)
        self.cpf_field.grid(column=1, row=0)

        self.return_button: ttk.Button = ttk.Button(self.frm, text="voltar")
        self.return_button.grid(column=0, row=1)

        self.remove_button: ttk.Button = ttk.Button(self.frm, text="remover")
        self.remove_button.grid(column=1, row=1)

    def set_confirm_action(self, callback):
        self.remove_button.config(command=callback)

    def set_return_action(self, callback):
        self.return_button.config(command=callback)

    def get_cpf_field(self):
        return self.cpf_field.get()
