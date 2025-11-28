from View.TelaExternos import TelaExternos

class ExternosController:
    def __init__(self, root, usuario):
        # Instancia a View passando a janela principal e o nome recuperado do banco

        self.view = TelaExternos(root, usuario)
      
        self.view.configurar_navegacao(
            self.abrir_dados,
            self.abrir_historico,
            
        )

    def abrir_dados(self):
        self.view.frm.destroy()
        # FuncionariosController(self.view.janela)

    def abrir_historico(self):
        self.view.frm.destroy()
        # PacientesController(self.view.janela)








    #def abrir_profissionais(self):
       # self.view.frm.destroy()
        # ProfissionaisController(self.view.janela)

    #def abrir_entradas(self):
        #self.view.frm.destroy()
        # EntradasController(self.view.janela)
    
    #def abrir_hospitais(self):
        #self.view.frm.destroy()
        # HospitaisController(self.view.janela)

