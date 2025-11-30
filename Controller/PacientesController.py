from tkinter import messagebox
from View.TelaPacientes import TelaPacientes
from Model.PacienteDAO import PacienteDAO

class PacientesController:
    def __init__(self, root, dados_usuario):
        self.usuario = dados_usuario # Guardamos o dicionário do funcionário para voltar depois
        
        # 1. Cria a View
        self.view = TelaPacientes(root)
        
        # 2. Cria o DAO (que você vai implementar)
        self.dao = PacienteDAO()

        # 3. Liga os botões da View às funções deste Controller
        self.view.configurar_botoes(
            self.cadastrar,
            self.remover,
            self.consultar_historico,
            self.voltar
        )
    senhar = "Paciente"
    
    def cadastrar(self):
        # Pega todos os dados da tela
        cpf = self.view.get_cpf()
        nome = self.view.get_nome()
        data = self.view.get_data()
        sexo = self.view.get_sexo()
        senha = PacientesController.senhar

        # Validação básica
        if not cpf or not nome:
            messagebox.showwarning("Aviso", "CPF e Nome são obrigatórios.")
            return

        # Chama o DAO para inserir no banco
        if self.dao.cadastrar(cpf, nome, data, sexo, senha):
            messagebox.showinfo("Sucesso", f"Paciente {nome} cadastrado com sucesso!")
            # Limpa os campos após cadastrar (opcional)
            # self.view.ent_nome.delete(0, 'end')
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar. Verifique se o CPF já existe.")

    def remover(self):
        cpf = self.view.get_cpf()
        if not cpf:
            messagebox.showwarning("Aviso", "Digite o CPF do paciente que deseja remover.")
            return
        
        # Confirmação de segurança (Boa prática!)
        resposta = messagebox.askyesno("Confirmar Exclusão", 
                                     f"Tem certeza que deseja apagar o paciente CPF {cpf}?\n\nIsso pode acionar registros de auditoria.")
        
        if resposta:
            self.dao.remover(cpf)
               

    def consultar_historico(self):
        cpf = self.view.get_cpf()
        if not cpf:
            messagebox.showwarning("Aviso", "Digite o CPF para buscar o histórico.")
            return

        # Busca no DAO (Espera-se que retorne uma lista de tuplas)
        resultados = self.dao.buscar_historico_entradas(cpf)
        
        if not resultados:
            messagebox.showinfo("Info", "Nenhum histórico encontrado para este CPF.")
        
        # Manda a View atualizar a tabela visual
        self.view.atualizar_tabela(resultados)

    def voltar(self):
        # Import local para evitar ciclo de importação
        from Controller.InternosController import InternosController
        
        self.view.frm.destroy()
        # Passa de volta o dicionário com os dados do funcionário logado
        InternosController(self.view.janela, self.usuario)