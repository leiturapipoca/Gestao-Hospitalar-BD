from tkinter import *
from tkinter import ttk

class TelaRemoverProf:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Remover Profissional de Saúde")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        # CPF label and entry field
        ttk.Label(self.frm, text="CPF:").grid(column=0, row=0, pady=10, sticky=W)
        self.campo_cpf = ttk.Entry(self.frm, width=20)
        self.campo_cpf.grid(column=1, row=0, pady=10)

        # Remover button
        self.btn_remover = ttk.Button(self.frm, text="Remover")
        self.btn_remover.grid(column=0, row=1, columnspan=2, pady=10)

        # Voltar button
        self.btn_voltar = ttk.Button(self.frm, text="Voltar")
        self.btn_voltar.grid(column=0, row=2, columnspan=2, pady=5)

        # Status message label
        self.lbl_status = ttk.Label(self.frm, text="", foreground="blue")
        self.lbl_status.grid(column=0, row=3, columnspan=2, pady=10)

    def set_action_remover(self, callback):
        """Set the callback function for the Remover button"""
        self.btn_remover.config(command=callback)

    def set_action_voltar(self, callback):
        """Set the callback function for the Voltar button"""
        self.btn_voltar.config(command=callback)

    def get_cpf(self):
        """Get the CPF value from the entry field"""
        return self.campo_cpf.get()

    def show_success_message(self, message: str):
        """Display a success message in green"""
        self.lbl_status.config(text=message, foreground="green")

    def show_error_message(self, message: str):
        """Display an error message in red"""
        self.lbl_status.config(text=message, foreground="red")

    def clear_form(self):
        """Clear the CPF entry field and status message"""
        self.campo_cpf.delete(0, END)
        self.lbl_status.config(text="")
