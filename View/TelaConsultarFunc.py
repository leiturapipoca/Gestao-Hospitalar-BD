from tkinter import *
from tkinter import ttk


class TelaConsultarFunc:
    def __init__(self, root: Tk, nome: str, cpf: str, funcao: str, matricula: str, hospitais_func: list[str]):
        self.nome = nome
        self.cpf = cpf
        self.funcao = funcao
        self.matricula = matricula
        self.hospitais_func = hospitais_func
        self.janela = root
        self.render_view()

    def render_view(self):
        self.janela.title("Consulta a Funcionário")
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="Pesquisar por CPF:").grid(column=0, row=0)
        self.input_cpf = ttk.Entry(self.frm, width=20)
        self.input_cpf.grid(column=1, row=0)


        ttk.Label(self.frm, text="Pesquisar por nome:").grid(column=0, row=1)
        self.input_cpf = ttk.Entry(self.frm, width=20)
        self.input_cpf.grid(column=1, row=1)

        self.search_by_cpf_button: ttk.Button = ttk.Button(self.frm, text="Pesquisar por Cpf")
        self.search_by_cpf_button.grid(column=0, row=2, pady=10)

        self.search_by_name_button: ttk.Button = ttk.Button(self.frm, text="Pesquisar por nome")
        self.search_by_name_button.grid(column=1, row=2, pady=10)

        ttk.Separator(self.frm, orient=HORIZONTAL).grid(row=3, columnspan=2, sticky=EW, pady=10)

        ttk.Label(self.frm, text="Nome funcionário:").grid(column=0, row=4) 
        ttk.Label(self.frm, text=self.nome).grid(column=1, row=4)

        ttk.Label(self.frm, text="Cpf funcionário:").grid(column=0, row=5)
        ttk.Label(self.frm, text=self.cpf).grid(column=1, row=5)

        ttk.Label(self.frm, text="Matricula funcionário:").grid(column=0, row=6)
        ttk.Label(self.frm, text=self.matricula).grid(column=1, row=6)

        ttk.Label(self.frm, text="Função:").grid(column=0, row=7)
        ttk.Label(self.frm, text=self.funcao).grid(column=1, row=7)

        
        columns = ("hosps")
        tree = ttk.Treeview(self.frm, columns=columns, show='headings', height=8)
        tree.heading('hosps', text='hospitais no qual trabalha')
        tree.column('hosps', width=200)
        tree.grid(row=9, columnspan=2)

        for hp in self.hospitais_func:
            tree.insert('', 'end', values=[hp])

        self.return_button: ttk.Button = ttk.Button(self.frm, text="voltar")
        self.return_button.grid(columnspan=2, row=10)


    def set_return_action(self, callback):
        self.return_button.config(command=callback)

    def set_search_by_cpf_action(self, callback):
        self.search_by_cpf_button.config(command=callback)

    def sef_search_by_name_action(self, callback):
        self.search_by_name_button.config(command=callback)

