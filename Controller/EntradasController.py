from tkinter import messagebox, END
from View.TelaEntradas import TelaEntradas
from Model.EntradaDAO import EntradaDAO
import Model.HospitalDAO as HospitalDAO 

# Importa os próximos passos do fluxo
from Controller.ProcedimentosController import ProcedimentosController
#from Controller.InternosController import InternosController

class EntradasController:
    def __init__(self, root, usuario):
        self.view = TelaEntradas(root)
        self.dao = EntradaDAO()
        

        
        # 'usuario' deve ser o dicionário: {'matricula': 1, 'nome': 'Carlos'}
        self.usuario = usuario 
        self.cnes_vinculado = None 

        print(f"[DEBUG] EntradasController iniciou com usuário: {self.usuario}")
        
        self.preencher_hospital_automatico()

        # Liga os botões às funções
        self.view.set_action_salvar(self.salvar_e_avancar)
        self.view.set_action_voltar(self.voltar)

    def preencher_hospital_automatico(self):
        # Validação de segurança para garantir que temos os dados
        if not isinstance(self.usuario, dict):
            print("Erro: Dados do usuário inválidos no EntradasController")
            return

        matricula = self.usuario.get('matricula')
        if not matricula: 
            messagebox.showerror("Erro", "Matrícula do funcionário não encontrada.")
            return

        # Busca o CNES usando a matrícula
        cnes = HospitalDAO.get_cnes_by_matricula(matricula, self.dao.connection)
        
        if cnes:
            self.cnes_vinculado = cnes
            # Busca o Nome do Hospital para exibir na tela (estética)
            nome_hosp = HospitalDAO.get_name_by_cnes(cnes, self.dao.connection)
            texto = nome_hosp if nome_hosp else cnes
            
            # Chama o método da View que preenche e trava o campo
            self.view.preencher_cnes(texto)
        else:
            messagebox.showwarning("Aviso", "Funcionário sem vínculo hospitalar.")

    def salvar_e_avancar(self):
        cpf = self.view.get_cpf()
        # Usamos o código CNES guardado na memória, não o texto da tela
        cnes_salvar = self.cnes_vinculado
        entry = self.view.get_description()
        if not cpf or not cnes_salvar:
            messagebox.showwarning("Aviso", "Preencha o CPF e verifique o hospital!")
            return
        
        # Chama o DAO e espera receber o ID da nova entrada (ex: 55)
        # Nota: O DAO deve estar configurado com 'RETURNING CODIGO'
        id_entrada = self.dao.registrar_entrada(cpf, cnes_salvar, entry)

        if id_entrada:
            # Sucesso! Destrói a tela atual
            self.view.frm.destroy()
            
            # Avança para a tela de Procedimentos
            # Passamos: Janela, Usuário (para voltar depois) e o ID da Entrada criada
            ProcedimentosController(self.view.janela, self.usuario, id_entrada)
            
        else:
            messagebox.showerror("Erro", "Falha ao registrar entrada. Verifique se o CPF existe.")

    def voltar(self):
        from Controller.InternosController import InternosController
        self.view.frm.destroy()
        # Volta para o menu anterior, devolvendo o dicionário do usuário
        InternosController(self.view.janela, self.usuario)