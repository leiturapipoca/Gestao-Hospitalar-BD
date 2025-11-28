# Controller/LoginController.py
from tkinter import messagebox
from View.TelaLogin import TelaLogin
from Model.UsuarioDAO import UsuarioDAO

class LoginController:
    def __init__(self, root):

        self.view = TelaLogin(root)
        self.view.set_action_botao(self.fazer_login)
        
      
        self.usuario_dao = UsuarioDAO()

    def fazer_login(self):
        print("O BOTÃO FOI CLICADO! CHEGOU NO CONTROLLER.")
        login_input = self.view.get_login() 
        senha_input = self.view.get_senha() 

        
        if not login_input.isdigit():
            messagebox.showwarning("Aviso", "ID ou Senha inválidos.")
            return


        autenticado = self.usuario_dao.autenticar(int(login_input), senha_input)
        if autenticado:
            messagebox.showinfo("Sucesso", "Login realizado!")
            #tela de menu
        else:
            messagebox.showerror("Erro", "ID ou Senha inválidos.")