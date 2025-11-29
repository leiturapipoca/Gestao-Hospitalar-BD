from View.TelaInternos import TelaInternos
from Controller.EntradasController import EntradasController
from Controller.GerenciarFuncsController import GerenciarFuncsController
from Controller.GerenciarProfsController import GerenciarProfsController

# from Controller.FuncionariosController import FuncionariosController
# from Controller.PacientesController import PacientesController
# from Controller.HospitaisController import HospitaisController

class InternosController:
    def __init__(self, root, dados_usuario):
        # 1. BLINDAGEM: Garante que 'dados_usuario' é o dicionário completo
        if isinstance(dados_usuario, dict):
            self.dados_usuario_completo = dados_usuario
            nome_exibir = dados_usuario['nome']
        else:
            # Recuperação de falha
            self.dados_usuario_completo = {"matricula": 0, "nome": str(dados_usuario)}
            nome_exibir = str(dados_usuario)

        # 2. Instancia a tela
        self.view = TelaInternos(root, nome_exibir)
        
        # 3. Configura a navegação
        self.view.configurar_navegacao(
            self.abrir_funcionarios,
            self.abrir_pacientes,
            self.abrir_profissionais,
            self.abrir_entradas,
            self.abrir_hospitais
        )

    def abrir_funcionarios(self):
        self.view.frm.destroy()
        GerenciarFuncsController(self.view.janela)

    def abrir_pacientes(self):
        self.view.frm.destroy()
        # PacientesController(self.view.janela)

    def abrir_profissionais(self):
        self.view.frm.destroy()
        GerenciarProfsController(self.view.janela, self.dados_usuario_completo)

    def abrir_entradas(self):
        self.view.frm.destroy()
        # Passa o dicionário completo para frente
        EntradasController(self.view.janela, self.dados_usuario_completo)
    
    def abrir_hospitais(self):
        self.view.frm.destroy()
        # HospitaisController(self.view.janela)
