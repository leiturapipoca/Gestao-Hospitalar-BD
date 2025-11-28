# Controller/LoginController.py
from tkinter import messagebox
from View.TelaLogin import TelaLogin
from Model.FuncionarioDAO import FuncionarioDAO
from Model.PacienteDAO import PacienteDAO
from Model.ProfissionalDAO import ProfissionalDAO
from Controller.InternosController import InternosController


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
            autenticado = self.funcionario_dao.autenticar(int(login_input), senha_input)

            if autenticado:
                messagebox.showinfo("Sucesso", "Funcionário logado")
                self.view.frm.destroy()
                InternosController(self.view.janela, autenticado)
                #tela de menuFuncionário

            else:
                messagebox.showerror("Erro", "ID ou Senha inválidos.")



        elif perfil_input == "PACIENTE":
            autenticado = self.paciente_dao.autenticar((login_input), senha_input)
            if autenticado:
                messagebox.showinfo("Sucesso", "Paciente logado")
                #tela de menuPaciente

            else:
                messagebox.showerror("Erro", "ID ou Senha inválidos.")


        else:
            
            autenticado = self.profissional_dao.autenticar((login_input), senha_input)
            if autenticado:
                messagebox.showinfo("Sucesso", "Profissional logado")
                self.view.frm.destroy()
                InternosController(self.view.janela, autenticado)
                #tela de menuProfissional
            else:
                messagebox.showerror("Erro", "ID ou Senha inválidos.")

            



     