# Controller/LoginController.py
from tkinter import messagebox
from View.TelaLogin import TelaLogin
from Model.FuncionarioDAO import FuncionarioDAO
from Model.PacienteDAO import PacienteDAO
from Model.ProfissionalDAO import ProfissionalDAO
from Controller.InternosController import InternosController
from Controller.ExternosController import ExternosController

# novo: import para abrir a tela de perfil do paciente
from Controller.PacientePerfilController import PacientePerfilController

class LoginController:
    def __init__(self, root):
        self.view = TelaLogin(root)
        self.view.set_action_botao(self.fazer_login)
        
        self.funcionario_dao = FuncionarioDAO()
        self.paciente_dao = PacienteDAO()
        self.profissional_dao = ProfissionalDAO()

    def fazer_login(self):
        login_input = self.view.get_login() 
        senha_input = self.view.get_senha() 
        perfil_input = self.view.get_tipo_usuario()

        if perfil_input == "FUNCIONARIO":
            # seu fluxo de funcionário (mantive int como você tinha)
            try:
                autenticado = self.funcionario_dao.autenticar(int(login_input), senha_input)
            except Exception as e:
                autenticado = False
                print(f"[LoginController] Erro autenticando funcionário: {e}")

            if autenticado:
                messagebox.showinfo("Sucesso", "Funcionário logado")
                self.view.frm.destroy()
                InternosController(self.view.janela, autenticado)
            else:
                messagebox.showerror("Erro", "ID ou Senha inválidos.")

        elif perfil_input == "PACIENTE":
            # tenta autenticar como paciente
            try:
                autenticado = self.paciente_dao.autenticar(login_input, senha_input)
            except Exception as e:
                print(f"[LoginController] Erro ao autenticar paciente: {e}")
                autenticado = False

            # Se a autenticação retornou um dicionário com os dados do paciente, usamos direto
            paciente_dict = None
            if autenticado and isinstance(autenticado, dict):
                paciente_dict = autenticado
            elif autenticado:
                # fallback: autenticado truthy mas não um dict -> tenta buscar os dados pelo CPF
                try:
                    paciente_dict = self.paciente_dao.buscar_por_cpf(login_input)
                except Exception as e:
                    print(f"[LoginController] Erro no fallback buscar_por_cpf: {e}")
                    paciente_dict = None

            if paciente_dict:
                messagebox.showinfo("Sucesso", "Paciente logado")
                # destrói o frame de login e abre o perfil do paciente
                self.view.frm.destroy()
                PacientePerfilController(self.view.janela, paciente_dict, use_toplevel=False)

                # se você preferir abrir também o menu de externos (tela de ações do paciente),
                # descomente a linha abaixo:
                # ExternosController(self.view.janela, paciente_dict)

            else:
                messagebox.showerror("Erro", "ID ou Senha inválidos.")

        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido.")
