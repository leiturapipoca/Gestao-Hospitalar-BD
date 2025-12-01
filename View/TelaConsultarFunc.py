from tkinter import *
from tkinter import ttk


class TelaConsultarFunc:
    def __init__(self, root: Tk, nome: str, cpf: str, funcao: str, matricula: str, hospitais_func: list[str]):
        self.janela = root
        self.janela.title("Consulta a Funcionário")
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="Nome funcionário:").grid(column=0, row=0)        
        ttk.Label(self.frm, text=nome).grid(column=1, row=0)

        ttk.Label(self.frm, text="Cpf funcionário:").grid(column=0, row=1)
        ttk.Label(self.frm, text=cpf).grid(column=1, row=1)

        ttk.Label(self.frm, text="Matricula funcionário:").grid(column=0, row=2)
        ttk.Label(self.frm, text=matricula).grid(column=1, row=2)

        ttk.Label(self.frm, text="Função:").grid(column=0, row=3)
        ttk.Label(self.frm, text=funcao).grid(column=1, row=3)

                
        columns = ("hosps")
        tree = ttk.Treeview(self.frm, columns=columns, show='headings', height=5)
        tree.heading('hosps', text='hospitais no qual trabalha')
        tree.column('hosps', width=200)
        tree.grid(row=4, columnspan=2)

        for hp in hospitais_func:
            tree.insert('', 'end', values=[hp])

        self.return_button: ttk.Button = ttk.Button(self.frm, text="voltar")
        self.return_button.grid(columnspan=2, row=5)

    def set_return_action(self, callback):
        self.return_button.config(command=callback)
