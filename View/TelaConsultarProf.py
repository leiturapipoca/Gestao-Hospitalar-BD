from tkinter import *
from tkinter import ttk

class TelaConsultarProf:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Consultar Profissional de Saúde")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        # CPF label and entry field
        ttk.Label(self.frm, text="CPF:").grid(column=0, row=0, pady=10, sticky=W)
        self.campo_cpf = ttk.Entry(self.frm, width=20)
        self.campo_cpf.grid(column=1, row=0, pady=10)

        # Consultar button
        self.btn_consultar = ttk.Button(self.frm, text="Consultar")
        self.btn_consultar.grid(column=0, row=1, columnspan=2, pady=10)

        # Voltar button
        self.btn_voltar = ttk.Button(self.frm, text="Voltar")
        self.btn_voltar.grid(column=0, row=2, columnspan=2, pady=5)

        # Results display frame
        self.frm_results = ttk.Frame(self.frm, padding=10)
        self.frm_results.grid(column=0, row=3, columnspan=2, pady=10, sticky=(W, E))

        # Result labels (initially empty)
        self.lbl_nome = ttk.Label(self.frm_results, text="")
        self.lbl_nome.grid(column=0, row=0, pady=5, sticky=W)

        self.lbl_tipo = ttk.Label(self.frm_results, text="")
        self.lbl_tipo.grid(column=0, row=1, pady=5, sticky=W)

        self.lbl_identificador = ttk.Label(self.frm_results, text="")
        self.lbl_identificador.grid(column=0, row=2, pady=5, sticky=W)

        # Status/error message label
        self.lbl_status = ttk.Label(self.frm, text="", foreground="blue")
        self.lbl_status.grid(column=0, row=4, columnspan=2, pady=10)

    def set_action_consultar(self, callback):
        """Set the callback function for the Consultar button"""
        self.btn_consultar.config(command=callback)

    def set_action_voltar(self, callback):
        """Set the callback function for the Voltar button"""
        self.btn_voltar.config(command=callback)

    def get_cpf(self):
        """Get the CPF value from the entry field"""
        return self.campo_cpf.get()

    def display_results(self, professional_data: dict):
        """Display the professional information in the results frame"""
        self.clear_results()
        
        if professional_data:
            nome = professional_data.get('nome', '')
            tipo = professional_data.get('tipo', '')
            
            self.lbl_nome.config(text=f"Nome: {nome}")
            
            if tipo == 'M':
                self.lbl_tipo.config(text="Tipo: Médico")
                crm = professional_data.get('crm', '')
                self.lbl_identificador.config(text=f"CRM: {crm}")
            elif tipo == 'E':
                self.lbl_tipo.config(text="Tipo: Enfermeiro")
                codigo = professional_data.get('codigo', '')
                self.lbl_identificador.config(text=f"CODIGO: {codigo}")

    def show_error_message(self, message: str):
        """Display an error message in red"""
        self.lbl_status.config(text=message, foreground="red")

    def clear_results(self):
        """Clear the results display and status message"""
        self.lbl_nome.config(text="")
        self.lbl_tipo.config(text="")
        self.lbl_identificador.config(text="")
        self.lbl_status.config(text="")
