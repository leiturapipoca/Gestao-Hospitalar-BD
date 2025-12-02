from tkinter import *
from tkinter import ttk

class TelaLiberarSala:
    def __init__(self, root, salas):
        self.root = root
        self.frm: ttk.Frame = ttk.Frame(root, padding=20)
        self.frm.grid()

        combo = ttk.Combobox(self.frm, width=100)
        combo.grid(column=0, row=0)
        combo['values'] = salas
        

        self.btn_return: ttk.Button = ttk.Button(self.frm, text="voltar")
        self.btn_return.grid(column=0, row=1)

    def set_action_return(self, callback):
        self.btn_return.config(command=callback)
