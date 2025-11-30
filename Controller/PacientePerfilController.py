# Controller/PacientePerfilController.py
from View.TelaPacientePerfil import TelaPacientePerfil
from Model.PacienteDAO import PacienteDAO
from tkinter import messagebox

class PacientePerfilController:
    def __init__(self, root, paciente_dict, use_toplevel=True):
        """
        paciente_dict = dicionário retornado por PacienteDAO.autenticar() ou buscar_por_cpf()
        use_toplevel=False -> usa a janela raiz (substitui o login)
        use_toplevel=True  -> abre uma janela Toplevel (comportamento antigo)
        """
        self.root = root
        self.paciente = paciente_dict
        self.view = TelaPacientePerfil(root, use_toplevel=use_toplevel)
        self.dao = PacienteDAO()

        # popula os dados básicos imediatamente
        self.view.set_dados_pessoais(self.paciente)

        # carrega listas do banco
        self._carregar_telefones()
        self._carregar_doencas()
        self._carregar_entradas()
        self._carregar_procedimentos()

    def _carregar_telefones(self):
        try:
            telefones = self.dao.get_telefones(self.paciente['cpf'])
            self.view.set_telefones(telefones)
        except Exception as e:
            print(f"[PacientePerfilController] Erro ao carregar telefones: {e}")

    def _carregar_doencas(self):
        try:
            doencas = self.dao.get_doencas(self.paciente['cpf'])
            self.view.set_doencas(doencas)
        except Exception as e:
            print(f"[PacientePerfilController] Erro ao carregar doenças: {e}")

    def _carregar_entradas(self):
        try:
            entradas = self.dao.get_entradas(self.paciente['cpf'])
            self.view.set_entradas(entradas)
        except Exception as e:
            print(f"[PacientePerfilController] Erro ao carregar entradas: {e}")

    def _carregar_procedimentos(self):
        try:
            procs = self.dao.get_procedimentos_por_cpf(self.paciente['cpf'])
            self.view.set_procedimentos(procs)
        except Exception as e:
            print(f"[PacientePerfilController] Erro ao carregar procedimentos: {e}")
