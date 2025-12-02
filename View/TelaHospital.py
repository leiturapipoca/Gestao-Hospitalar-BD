from tkinter import *
from tkinter import ttk

class TelaHospital:
    def __init__(self, root: Tk):
        self.root = root
        self.frm = ttk.Frame(root, padding=20)
        self.frm.grid()

        self.btn_salas: ttk.Button = ttk.Button(self.frm, text="liberar salas")
        self.btn_salas.grid(column=0, row=0)
        self.btn_hosps: ttk.Button = ttk.Button(self.frm, text="listar hospitais")
        self.btn_hosps.grid(column=0, row=1)

        self.btn_return: ttk.Button = ttk.Button(self.frm, text="voltar")
        self.btn_return.grid(column=0, row=2)

    def set_action_salas(self, callback):
        self.btn_salas.config(command=callback)

    def set_action_hosps(self, callback):
        self.btn_hosps.config(command=callback)

    def set_action_return(self, callback):
        self.btn_return.config(command=callback)
