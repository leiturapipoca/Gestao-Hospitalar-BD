from tkinter import *
from tkinter import ttk

class TelaLiberarSala:
    def __init__(self, root, salas_ocupadas):
        self.janela = root
        self.frm = ttk.Frame(root, padding=20)
        self.frm.grid()

        ttk.Label(self.frm, text="Liberar Sala (Check-out)", font=("Arial", 14)).grid(column=0, row=0, pady=10)
        
        ttk.Label(self.frm, text="Selecione a sala para liberar:").grid(column=0, row=1, sticky=W)
        
        # Combobox com as salas ocupadas
        self.combo_salas = ttk.Combobox(self.frm, width=30, state='readonly')
        self.combo_salas['values'] = salas_ocupadas
        self.combo_salas.grid(column=0, row=2, pady=5)

        # Botão Liberar
        self.btn_liberar = ttk.Button(self.frm, text="LIBERAR SALA")
        self.btn_liberar.grid(column=0, row=3, pady=10, sticky=EW)

        # Botão Voltar
        self.btn_return = ttk.Button(self.frm, text="Voltar")
        self.btn_return.grid(column=0, row=4, pady=5, sticky=EW)

    def set_action_liberar(self, callback):
        self.btn_liberar.config(command=callback)

    def set_action_return(self, callback):
        self.btn_return.config(command=callback)
        
    def get_sala_selecionada(self):
        return self.combo_salas.get()