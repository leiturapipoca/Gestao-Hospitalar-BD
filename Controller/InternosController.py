from View.TelaInternos import TelaInternos

class InternosController:
    def __init__(self, root, usuario):
        # Instancia a View passando a janela principal e o nome recuperado do banco

        self.view = TelaInternos(root, usuario)
      
        self.view.configurar_navegacao(
            self.abrir_funcionarios,
            self.abrir_pacientes,
            self.abrir_profissionais,
            self.abrir_entradas,
            self.abrir_hospitais
        )

    def abrir_funcionarios(self):
        self.view.frm.destroy()
        # FuncionariosController(self.view.janela)

    def abrir_pacientes(self):
        self.view.frm.destroy()
        # PacientesController(self.view.janela)

    def abrir_profissionais(self):
        self.view.frm.destroy()
        # ProfissionaisController(self.view.janela)

    def abrir_entradas(self):
        self.view.frm.destroy()
        # EntradasController(self.view.janela)
    
    def abrir_hospitais(self):
        self.view.frm.destroy()
        # HospitaisController(self.view.janela)

