from tkinter import *
from tkinter import ttk

class TelaAdicionarProf:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Adicionar Profissional de Saúde")
        
        self.frm = ttk.Frame(self.janela, padding=20)
        self.frm.grid()

        # CPF label and entry field
        ttk.Label(self.frm, text="CPF:").grid(column=0, row=0, pady=10, sticky=W)
        self.campo_cpf = ttk.Entry(self.frm, width=20)
        self.campo_cpf.grid(column=1, row=0, pady=10)

        # Nome label and entry field
        ttk.Label(self.frm, text="Nome:").grid(column=0, row=1, pady=10, sticky=W)
        self.campo_nome = ttk.Entry(self.frm, width=30)
        self.campo_nome.grid(column=1, row=1, pady=10)

        # Tipo label and radio buttons
        ttk.Label(self.frm, text="Tipo:").grid(column=0, row=2, pady=10, sticky=W)
        self.tipo_var = StringVar(value="M")
        
        tipo_frame = ttk.Frame(self.frm)
        tipo_frame.grid(column=1, row=2, pady=10, sticky=W)
        
        ttk.Radiobutton(tipo_frame, text="Médico (M)", variable=self.tipo_var, 
                       value="M", command=self.on_tipo_change).pack(side=LEFT, padx=5)
        ttk.Radiobutton(tipo_frame, text="Enfermeiro (E)", variable=self.tipo_var, 
                       value="E", command=self.on_tipo_change).pack(side=LEFT, padx=5)

        # CRM label and entry field (for Médico)
        self.lbl_crm = ttk.Label(self.frm, text="CRM:")
        self.lbl_crm.grid(column=0, row=3, pady=10, sticky=W)
        self.campo_crm = ttk.Entry(self.frm, width=20)
        self.campo_crm.grid(column=1, row=3, pady=10)

        # CODIGO label and entry field (for Enfermeiro)
        self.lbl_codigo = ttk.Label(self.frm, text="CODIGO:")
        self.campo_codigo = ttk.Entry(self.frm, width=20)

        # Adicionar button
        self.btn_adicionar = ttk.Button(self.frm, text="Adicionar")
        self.btn_adicionar.grid(column=0, row=4, columnspan=2, pady=10)

        # Voltar button
        self.btn_voltar = ttk.Button(self.frm, text="Voltar")
        self.btn_voltar.grid(column=0, row=5, columnspan=2, pady=5)

        # Status message label
        self.lbl_status = ttk.Label(self.frm, text="", foreground="blue")
        self.lbl_status.grid(column=0, row=6, columnspan=2, pady=10)

        # Initialize with Médico fields visible
        self.on_tipo_change()

    def on_tipo_change(self):
        """Show/hide CRM or CODIGO fields based on selected type"""
        tipo = self.tipo_var.get()
        
        if tipo == "M":
            # Show CRM, hide CODIGO
            self.lbl_crm.grid(column=0, row=3, pady=10, sticky=W)
            self.campo_crm.grid(column=1, row=3, pady=10)
            self.lbl_codigo.grid_remove()
            self.campo_codigo.grid_remove()
        else:  # tipo == "E"
            # Hide CRM, show CODIGO
            self.lbl_crm.grid_remove()
            self.campo_crm.grid_remove()
            self.lbl_codigo.grid(column=0, row=3, pady=10, sticky=W)
            self.campo_codigo.grid(column=1, row=3, pady=10)

    def set_action_adicionar(self, callback):
        """Set the callback function for the Adicionar button"""
        self.btn_adicionar.config(command=callback)

    def set_action_voltar(self, callback):
        """Set the callback function for the Voltar button"""
        self.btn_voltar.config(command=callback)

    def get_form_data(self):
        """Get all form data as a dictionary"""
        tipo = self.tipo_var.get()
        data = {
            'cpf': self.campo_cpf.get(),
            'nome': self.campo_nome.get(),
            'tipo': tipo
        }
        
        if tipo == "M":
            data['crm'] = self.campo_crm.get()
        else:  # tipo == "E"
            data['codigo'] = self.campo_codigo.get()
        
        return data

    def show_success_message(self, message: str):
        """Display a success message in green"""
        self.lbl_status.config(text=message, foreground="green")

    def show_error_message(self, message: str):
        """Display an error message in red"""
        self.lbl_status.config(text=message, foreground="red")

    def clear_form(self):
        """Clear all form fields and status message"""
        self.campo_cpf.delete(0, END)
        self.campo_nome.delete(0, END)
        self.campo_crm.delete(0, END)
        self.campo_codigo.delete(0, END)
        self.tipo_var.set("M")
        self.on_tipo_change()
        self.lbl_status.config(text="")
