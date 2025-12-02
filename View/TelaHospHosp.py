from tkinter import *
from tkinter import ttk

class TelaHospHosp:
    def __init__(self, root: Tk, dados: list[tuple]):
        self.frm = ttk.Frame(root, padding=20)
        self.frm.grid()
        columns = ("hospital", "gerentes")
        self.tree: ttk.Treeview = ttk.Treeview(self.frm, columns=columns, show="headings", height=6)
        self.tree.heading("hospital", text="Código")
        self.tree.heading("gerentes", text="Data")
        self.tree.column("hospital", width=100)
        self.tree.column("gerentes", width=100)
        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.btn_return: ttk.Button = ttk.Button(self.frm, text="voltar")
        self.btn_return.grid(row=1, column=0)

        for dado in dados:
            self.tree.insert('', 'end', values=dado)

    def set_action_return(self, callback):
        self.btn_return.config(command=callback)
        

        
    
