from tkinter import messagebox
from View.TelaProcedimentos import TelaProcedimentos
from Model.ProcedimentosDAO import ProcedimentosDAO

class ProcedimentosController:
    def __init__(self, root, usuario, id_entrada):
        """
        Recebe:
        - usuario: Dicionário do funcionário logado (para voltar ao menu depois)
        - id_entrada: O ID da entrada recém-criada (Foreign Key para o procedimento)
        """
        self.usuario = usuario
        self.id_entrada = id_entrada 
        
        self.dao = ProcedimentosDAO()
        
        # 1. Busca os tipos reais no banco para preencher o Combobox
        # (Nada de dados 'hardcoded' como 'batata')
        lista_tipos = self.dao.get_tipos_procedimento()
        
        # 2. Cria a View passando a lista carregada
        self.view = TelaProcedimentos(root, lista_tipos)
        
        # 3. Configura os botões
        self.view.set_action_salvar(self.salvar_procedimento)
        self.view.set_action_voltar(self.voltar_menu)

    def salvar_procedimento(self):
        # Coleta os dados da tela
        doenca = self.view.get_doenca()
        crm_medico = self.view.get_cpf_medico()
        tipo_proc = self.view.get_procedimento()
        sala = self.view.get_sala() # Pega o número da sala

        # Validação Simples
        if not doenca or not crm_medico or not tipo_proc or not sala:
            messagebox.showwarning("Aviso", "Preencha todos os campos, incluindo a sala.")
            return
        
        # Validação se sala é número
        if not sala.isdigit():
             messagebox.showwarning("Aviso", "O número da sala deve ser numérico.")
             return

        # Chama o DAO com o novo parâmetro
        sucesso, mensagem = self.dao.registrar_procedimento_completo(
            self.id_entrada, 
            crm_medico, 
            tipo_proc, 
            doenca,
            int(sala) # Passa como inteiro
        )

    def voltar_menu(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        # Volta para o menu principal devolvendo os dados do funcionário
        InternosController(self.view.janela, self.usuario)