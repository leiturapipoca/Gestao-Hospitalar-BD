from tkinter import messagebox, filedialog
from View.TelaPerfilFuncionario import TelaPerfilFuncionario
from Model.FuncionarioDAO import FuncionarioDAO

class PerfilFuncionarioController:
    def __init__(self, root, dados_usuario):
        self.usuario_atual = dados_usuario
        self.view = TelaPerfilFuncionario(root, self.usuario_atual)
        self.dao = FuncionarioDAO()
        
        # Variável para guardar o caminho da foto se o usuário escolher uma
        self.caminho_foto = None

        self.view.configurar_botoes(
            self.salvar_tudo,
            self.voltar,
            self.selecionar_foto
        )

    def selecionar_foto(self):
        # Abre janela do Windows/Linux para pegar arquivo
        arquivo = filedialog.askopenfilename(
            title="Selecione sua foto",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
        )
        
        if arquivo:
            self.caminho_foto = arquivo
            # Atualiza o label na tela para mostrar que selecionou
            nome_arquivo = arquivo.split("/")[-1] # Pega só o nome (ex: foto.jpg)
            self.view.lbl_status_foto.config(text=f"Selecionado: {nome_arquivo}", foreground="green")

    def salvar_tudo(self):
        nome = self.view.get_nome()
        senha = self.view.get_senha()
        matricula = self.usuario_atual['matricula']

        if not nome or not senha:
            messagebox.showwarning("Aviso", "Nome e Senha são obrigatórios.")
            return

        # 1. Atualiza Texto
        sucesso_txt, msg_txt = self.dao.update_funcionario(matricula, nome, senha)
        
        # 2. Atualiza Foto (se tiver selecionado alguma)
        sucesso_foto = True
        if self.caminho_foto:
            sucesso_foto, msg_foto = self.dao.salvar_foto(matricula, self.caminho_foto)
            if not sucesso_foto:
                messagebox.showerror("Erro na Foto", msg_foto)

        # Resultado Final
        if sucesso_txt and sucesso_foto:
            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")
            self.usuario_atual['nome'] = nome # Atualiza localmente
            self.voltar()
        elif not sucesso_txt:
            messagebox.showerror("Erro", msg_txt)

    def voltar(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        InternosController(self.view.janela, self.usuario_atual)